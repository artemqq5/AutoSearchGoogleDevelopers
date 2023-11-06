import itertools
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager

from requests_html import HTMLSession

from db_manager import MainDataBase


def generate_combinations(alphabet, length):
    for comb in itertools.product(alphabet, repeat=length):
        yield ''.join(comb)


def worker(first_combination, second_combination, thrid_combination, session):
    # emails_list[0] = emails_list[0] + 1

    package = ""
    try:
        if thrid_combination is not None:
            url = f"https://play.google.com/store/apps/details?id={first_combination}.{second_combination}.{thrid_combination}"
            package = f"{first_combination}.{second_combination}.{thrid_combination}"
        elif second_combination is not None:
            url = f"https://play.google.com/store/apps/details?id={first_combination}.{second_combination}"
            package = f"{first_combination}.{second_combination}"
        else:
            url = f"https://play.google.com/store/apps/details?id={first_combination}"
            package = f"{first_combination}"

        r = session.get(url)
        about = r.html.find('.pSEeg')
        email = about[0].text
        phone_number = None

        for args in about:
            if "@" in args.text:
                email = args.text
            if "+" in args.text:
                phone_number = args.text

        print(f"({package})  -  {email}, {url}")
        MainDataBase().add_contact(email, phone_number)
        # emails_list.append(f"({package})  -  {email}, {url}")

    except Exception as e:
        print(f"{package} - none | {e}")
        pass


def main():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    session = HTMLSession()
    # manager = Manager()
    # emails_list = manager.list()
    # emails_list.append(0)

    with ProcessPoolExecutor(max_workers=1) as executor:
        for combinations_length in range(1, len(alphabet) + 1):
            for first_combination in generate_combinations(alphabet, combinations_length):
                executor.submit(worker, first_combination, None, None, session)
                for combinations_length2 in range(1, len(alphabet) + 1):
                    for second_combination in generate_combinations(alphabet, combinations_length2):
                        executor.submit(worker, first_combination, second_combination, None, session)
                        for combinations_length3 in range(1, len(alphabet) + 1):
                            for third_combination in generate_combinations(alphabet, combinations_length3):
                                executor.submit(worker, first_combination, second_combination, third_combination,
                                                session)

    # print(emails_list)


if __name__ == '__main__':
    main()
