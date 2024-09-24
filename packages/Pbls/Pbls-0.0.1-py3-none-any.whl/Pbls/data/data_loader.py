import hashlib
import os
import tarfile
from tqdm import tqdm
import paramiko  # SCP를 사용하기 위해 paramiko 사용
from getpass import getpass


def calculate_md5_last_64M(file_path, chunk_size=1024 * 1024):
    """
    대용량 파일의 마지막 64MB에 대한 MD5 체크섬을 계산하는 함수
    - file_path: 체크섬을 계산할 파일 경로
    - chunk_size: 한 번에 읽을 청크 크기 (기본값: 1MB)
    """
    md5 = hashlib.md5()  # MD5 해시 함수 생성
    
    # 파일 크기 확인
    try:
        file_size = os.path.getsize(file_path)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return None

    # 마지막 64MB 위치 계산 (64 * 1024 * 1024 = 67108864 바이트)
    last_64M_offset = max(0, file_size - 64 * 1024 * 1024)

    # 파일 열기
    with open(file_path, "rb") as f:
        # 마지막 64MB 부분으로 이동
        f.seek(last_64M_offset)
        
        # 마지막 64MB를 청크 단위로 읽어서 MD5 업데이트
        while chunk := f.read(chunk_size):
            md5.update(chunk)

    # 최종 MD5 해시값 반환
    return md5.hexdigest()


# 원격 서버에서 마지막 64MB의 체크섬을 계산하고 결과를 파일에 저장하는 함수
def remote_checksum_last_64M(ssh_client, remote_file_path, checksum_file_path):
    # 원격 서버에서 실행할 명령어
    # tail 명령을 통해 마지막 64MB를 읽고, 해당 데이터에 대해 체크섬을 계산하여 결과를 저장
    command = f"tail -c 67108864 {remote_file_path} | md5sum | awk '{{print $1}}' > {checksum_file_path}"

    stdin, stdout, stderr = ssh_client.exec_command(command)

    # 명령어 실행 결과와 에러 출력
    stdout_output = stdout.read().decode()
    stderr_output = stderr.read().decode()

    if stderr_output:
        print(f"Error: {stderr_output}")
    else:
        print(f"Checksum saved to: {checksum_file_path}")
        print(f"Command output: {stdout_output}")


# 원격 서버에서 tar 파일을 생성하고 진행 상황을 tqdm으로 표시하는 함수
def create_tar_with_progress(ssh_client, source_directory, tar_file_path):
    # 원격 디렉토리 크기를 계산하여 진행 상황을 표시하기 위한 정보 획득
    # tar 파일 생성 명령어
    command = f"tar -cvf {tar_file_path} -C {source_directory} ."
    stdin, stdout, stderr = ssh_client.exec_command(command)

    remained_update_count = 100000
    # 진행 상황을 표시하면서 tar 파일 생성
    with tqdm(total=remained_update_count, unit='P', desc="Creating tar") as pbar:
       while True:
            # tar 명령어의 표준 출력 읽기
            line = stdout.readline()
            if not line:
                pbar.update(remained_update_count)
                break
            if remained_update_count > 1:
                remained_update_count = remained_update_count - 1
                pbar.update(1)

    print(f"Tar file created: {tar_file_path}")

# 원격 서버에서 체크섬을 읽는 함수
def get_remote_checksum(ssh_client, checksum_file_path):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(f"cat {checksum_file_path}")
        checksum = stdout.read().decode().strip()
        if checksum:
            return checksum
    except:
        return None

# tar 파일의 존재 여부 및 체크섬 검증 후 tar 파일을 생성하는 함수
def check_and_create_tar(ssh_client, source_directory, tar_file_path, checksum_file_path):
    # tar 파일과 체크섬 파일 존재 여부 확인
    sftp = ssh_client.open_sftp()
    
    tar_exists = False
    checksum_exists = False
    
    try:
        sftp.stat(tar_file_path)
        tar_exists = True
    except FileNotFoundError:
        tar_exists = False

    try:
        sftp.stat(checksum_file_path)
        checksum_exists = True
    except FileNotFoundError:
        checksum_exists = False

    sftp.close()

    # tar 파일과 체크섬 파일이 모두 있는 경우, 체크섬을 비교
    if tar_exists and checksum_exists:
        remote_checksum = get_remote_checksum(ssh_client, checksum_file_path)
        command = f"tail -c 67108864 {tar_file_path} | md5sum | awk '{{print $1}}'"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        new_checksum = stdout.read().decode().strip()

        if new_checksum != remote_checksum:
            print("Checksums do not match. Deleting the tar file and regenerating.")
            ssh_client.exec_command(f"rm -f {tar_file_path} {checksum_file_path}")
            create_tar_with_progress(ssh_client, source_directory, tar_file_path)
            remote_checksum_last_64M(ssh_client, tar_file_path, checksum_file_path)
        else:
            print("Tar file and checksum are up to date.")
    else:
        # tar 파일이 없거나 체크섬 파일이 없으면 tar 파일을 생성하고 체크섬을 계산
        if tar_exists:
            ssh_client.exec_command(f"rm -f {tar_file_path}")
            print(f"Checksum file {checksum_file_path} does not exist. Regenerating checksum.")
        else:
            if checksum_exists:
                ssh_client.exec_command(f"rm -f {checksum_file_path}")
            print(f"Tar file {tar_file_path} does not exist. Creating tar file.")
        
        create_tar_with_progress(ssh_client, source_directory, tar_file_path)
        remote_checksum_last_64M(ssh_client, tar_file_path, checksum_file_path)


# 원격 파일의 크기 확인 함수
def get_remote_file_size(ssh_client, remote_file):
    sftp = ssh_client.open_sftp()
    file_size = sftp.stat(remote_file).st_size
    sftp.close()
    return file_size

# SFTP를 사용하여 파일 이어받기 구현 (tqdm 진행 표시 포함)
def sftp_resume_get(ssh_client, remote_file, local_file):
    sftp = ssh_client.open_sftp()

    # 로컬 파일이 존재하는 경우, 이미 다운로드된 부분의 크기를 확인
    if os.path.exists(local_file):
        local_file_size = os.path.getsize(local_file)
    else:
        local_file_size = 0

    # 원격 파일 크기 확인
    remote_file_size = get_remote_file_size(ssh_client, remote_file)

    # 로컬 파일이 이미 전부 다운로드된 경우 처리
    if local_file_size >= remote_file_size:
        print(f"파일이 이미 완전히 다운로드되었습니다: {local_file}")
        return

    # tqdm을 사용한 진행 상황 표시
    with tqdm(total=remote_file_size, initial=local_file_size, unit='B', unit_scale=True, desc=remote_file) as pbar:
        # 이어받기 모드로 파일 열기
        with open(local_file, 'ab') as f:
            # 원격 파일에서 이미 다운로드된 부분을 제외한 나머지 부분 다운로드
            sftp_file = sftp.file(remote_file, 'r')
            sftp_file.seek(local_file_size)  # 이미 다운로드된 부분 건너뛰기

            # 1MB씩 다운로드하여 로컬 파일에 추가 저장
            while local_file_size < remote_file_size:
                data = sftp_file.read(1024 * 1024)  # 1MB씩 읽기
                if not data:
                    break
                f.write(data)
                local_file_size += len(data)
                pbar.update(len(data))  # tqdm 진행 상황 업데이트

    print(f"다운로드 완료: {local_file}")
    sftp.close()

class DataSetInfo: pass

def get_dataset_info(username, password, dataset, server_ip, server_port):
    dataset_info = DataSetInfo()
    dataset_info.username = username
    dataset_info.password = password
    dataset_info.server_ip = server_ip
    dataset_info.server_port = server_port
    dataset_info.server = f'-p {server_port} {username}@{server_ip}'  # 서버 사용자 및 IP 주소
    dataset_info.remote_dir = f'/storage_data/projects/Data/InputData/{dataset}'  # 서버의 파일이 있는 디렉토리
    tar_file_name = f'{dataset}.tar'  # 서버에서 생성될 tar 파일 이름
    dataset_info.tar_file_name = tar_file_name
    dataset_info.remote_tar_path = f'/storage_data/projects/Data/InputData/99_tar/{tar_file_name}'  # 서버에서 tar 파일의 경로
    dataset_info.checksum_file_path = f'/storage_data/projects/Data/InputData/99_tar/{tar_file_name}.checksum_last_64M'
    dataset_info.local_tar_path = f'{tar_file_name}'  # 로컬에서 tar 파일을 저장할 경로

    return dataset_info

def get_data(di):
    "get data"
    #-----------------
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(di.server_ip, username=di.username, password=di.password, port=di.server_port)  # 인증서 사용 가능

    # 1. create_tar_on_server_if_needed()  
    # 서버에 tar 파일이 없으면 생성
    check_and_create_tar(ssh, di.remote_dir, di.remote_tar_path, di.checksum_file_path)

    # 2. copy_tar_to_local_with_resume()  
    # 로컬로 tar 파일 복사 (진행률 표시, 이어받기 지원)
    print("Copying tar file from server to local machine with resume support...")

    sftp_resume_get(ssh, di.remote_tar_path, di.local_tar_path)
    remote_checksum = get_remote_checksum(ssh, di.checksum_file_path)
    md5_checksum = calculate_md5_last_64M(di.local_tar_path)

    if remote_checksum != md5_checksum:
        print(f"redownload since hash diff: remote {remote_checksum} local {md5_checksum}")
        os.remove(di.local_tar_path)
        sftp_resume_get(ssh, di.remote_tar_path, di.local_tar_path)

    ssh.close()
    #-----------------

    # 3. extract_tar_locally()  
    # 로컬에서 tar 파일 해제 (진행률 표시)

    print(f"Extracting {di.local_tar_path} ...")

    # 파일 크기 확인
    tar_size = os.path.getsize(di.local_tar_path)
    
    # 진행률 표시
    with tarfile.open(di.local_tar_path, 'r') as tar:
        members = tar.getmembers()
        with tqdm(total=len(members), desc="Extracting", unit="file") as pbar:
            for member in members:
                tar.extract(member, path=os.path.splitext(di.local_tar_path)[0])
                pbar.update(1)
    
    print(f"Extraction complete.")


def get_data_test():

    # 실행 순서
    # 0. 서버 정보

    a_username='heeseok'
    a_password=getpass()
    # a_dataset='kistiroad'
    a_dataset='potholedl'
    a_server_ip = '220.90.239.100'
    a_server_port=122

    di = get_dataset_info(a_username, a_password, a_dataset, a_server_ip, a_server_port)

    get_data(di)

# get_data_test()
