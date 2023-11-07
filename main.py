import itertools
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager

from requests_html import HTMLSession

from db_manager import MainDataBase

user_list = [0]


def generate_combinations(alphabet, length):
    for comb in itertools.product(alphabet, repeat=length):
        yield ''.join(comb)


def worker(first_combination, second_combination, thrid_combination, session):
    user_list[0] = user_list[0] + 1

    package = ""
    if thrid_combination is not None:
        url = f"https://play.google.com/store/apps/details?id={first_combination}.{second_combination}.{thrid_combination}"
        package = f"{first_combination}.{second_combination}.{thrid_combination}"
    elif second_combination is not None:
        url = f"https://play.google.com/store/apps/details?id={first_combination}.{second_combination}"
        package = f"{first_combination}.{second_combination}"
    else:
        url = f"https://play.google.com/store/apps/details?id={first_combination}"
        package = f"{first_combination}"

    try:
        r = session.get(url)
        about = r.html.find('.pSEeg')
        email = about[0].text
        phone_number = None

        for args in about:
            if "@" in args.text:
                email = str(args.text)
            if "+" in args.text:
                phone_number = str(args.text)

        print(f"#{user_list[0]} ({package})  -  {email}, {phone_number}, {url}")
        MainDataBase().add_contact(email, phone_number, package)

    except Exception as e:
        print(f"#{user_list[0]} ({package}) - none | {e}")
        pass


def main():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    # alphabet = 'ai'
    session = HTMLSession()

    # searching only for one-two package
    for combinations_length in range(1, len(alphabet) + 1):
        for first_combination in generate_combinations(alphabet, combinations_length):
            worker(first_combination, None, None, session)
            for combinations_length2 in range(1, len(alphabet) + 1):
                for second_combination in generate_combinations(alphabet, combinations_length2):
                    worker(first_combination, second_combination, None, session)
                    # for combinations_length3 in range(1, len(alphabet) + 1):
                    #     for third_combination in generate_combinations(alphabet, combinations_length3):
                    #         worker(first_combination, second_combination, third_combination, session)

    print(user_list)


if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"time doing: {elapsed_time} seconds")
    