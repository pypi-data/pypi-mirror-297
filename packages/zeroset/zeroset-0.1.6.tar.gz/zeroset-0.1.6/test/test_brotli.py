import random

import brotli
import os
import concurrent.futures
import time
import multiprocessing
from zeroset import py0
import logging
from tqdm import tqdm

logging.getLogger('faker').setLevel(logging.ERROR)
from faker import Faker


def make_fake_dataset():
    fake_ko = Faker('ko-KR')
    fake_en = Faker('en_US')
    faker_instance = [
        "fake_ko", "fake_en"
    ]
    faker_methods = [
        "name",
        "email",
        "address",
        "user_name",
        "phone_number",
        "catch_phrase",
        "ipv4_private",
        "job",
        "company",
        "country"
    ]
    N = 10
    M = 1000000
    with open("../data/text_data4.txt", "at", encoding="utf-8") as f:
        with tqdm(total=N * M, desc="generate text file") as pbar:
            for k in range(20):
                for i in range(1000000):
                    pbar.update(1)
                    texts = []
                    for j in range(random.randint(1, 5)):
                        method_name = random.choice(faker_methods)
                        instance_name = random.choice(faker_instance)
                        text = eval(f"{instance_name}.{method_name}()")
                        texts.append(text)
                    f.write(",".join(texts) + "\n")
    print("filesize: ", py0.get_file_size("../data/text_data4.txt"))


def compress_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        data = file.read()

    compressed_data = brotli.compress(data)

    with open(output_file, 'wb') as file:
        file.write(compressed_data)


def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        compressed_data = file.read()

    decompressed_data = brotli.decompress(compressed_data)

    with open(output_file, 'wb') as file:
        file.write(decompressed_data)


def compress_chunk(chunk, quality=11):
    return brotli.compress(chunk, quality=quality)


def parallel_compress_file(input_file, output_file, chunk_size=1024 * 1024, max_workers=None, quality=11):
    start_time = time.time()

    # 파일 크기 확인
    file_size = os.path.getsize(input_file)

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 청크 단위로 파일을 읽고 압축 작업 제출
            futures = []
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                future = executor.submit(compress_chunk, chunk, quality)
                futures.append(future)

            # 압축된 청크를 순서대로 파일에 쓰기
            for future in concurrent.futures.as_completed(futures):
                compressed_chunk = future.result()
                f_out.write(compressed_chunk)

    end_time = time.time()
    print(f"압축 완료. 소요 시간: {end_time - start_time:.2f}초")
    print(f"원본 파일 크기: {file_size} 바이트")
    print(f"압축 파일 크기: {os.path.getsize(output_file)} 바이트")
    print(f"압축률: {(1 - os.path.getsize(output_file) / file_size) * 100:.2f}%")


def brotli_test01():
    original_file = "../data/tail.txt"
    compressed_file = os.path.splitext(original_file)[0] + ".br"
    decompressed_file = os.path.splitext(original_file)[0] + "_dc.txt"

    compress_file(original_file, compressed_file)
    print(f"{original_file}을 {compressed_file}로 압축했습니다.")

    # 압축 파일 압축 해제
    decompress_file(compressed_file, decompressed_file)
    print(f"{compressed_file}을 {decompressed_file}로 압축 해제했습니다.")
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)
    print(f"원본 파일 크기: {original_size} 바이트")
    print(f"압축 파일 크기: {compressed_size} 바이트")
    print(f"압축률: {(1 - compressed_size / original_size) * 100:.2f}%")


def brotli_test02():
    original_file = "R:/__COMPRESS_TEST__/TEXT/large.txt"
    compressed_file = original_file + ".br"
    max_workers = multiprocessing.cpu_count()
    parallel_compress_file(original_file, compressed_file, max_workers=max_workers)


def make_large_txt():
    with open("../data/head.txt", "rt", encoding="utf-8") as f:
        lines1 = f.read().splitlines()
    with open("../data/tail.txt", "rt", encoding="utf-8") as f:
        lines2 = f.read().splitlines()
    lines = lines1 + lines2

    rlines = []
    for line in lines:
        rline = line[::-1]
        rlines.append(rline)

    total_lines = lines + rlines
    with open("../data/large.txt", "wt", encoding="utf-8") as f:
        f.write("\n".join(total_lines))
    file_size = py0.get_file_size("../data/large.txt")
    print(f'file size: {file_size}')


if __name__ == '__main__':
    make_fake_dataset()
