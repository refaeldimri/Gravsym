import requests

#https://mattosmonuments.com/wp-content/uploads/2020/05/BM-341-scaled.jpg =====star of david
#
# https://www.westmemorials.com/Upload/Products/SubImages/be943e895f1d471989e44686d6bbaeb5.jpg ===star and candelabrum


def main():
    url = input("URL: ")
    response = requests.get("http://localhost/objectDetectionMultiModels.py?url=" + str(url))
    print(response.text)
    if "No identification" not in response.text:
            print("\nIs it right?\n1 - True\n2 - False")     
            ans = int(input("Enter Number: "))
            if ans == 2:
                response = requests.get("http://localhost/objectDetectionMultiModels.py?ans=False")
                print(response.text)


if __name__ == "__main__":
    main()
