def main():
    n = int(input())
    s = input()

    anton_count = 0
    danik_count = 0

    for char in s:
        if char == 'A':
            anton_count += 1
        elif char == 'D':
            danik_count += 1

    if anton_count > danik_count:
        print("Anton")
    elif danik_count > anton_count:
        print("Danik")
    else:
        print("Friendship")
