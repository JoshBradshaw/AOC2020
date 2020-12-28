def binary_search(search_range, selector):
    l, r = search_range
    if l == r:
        return l
    elif selector[0] == 'F' or selector[0] == 'L':
        return binary_search((l, l + (r-l)//2), selector[1:])
    else:
        return binary_search((l + (r-l)//2 + 1, r), selector[1:])

def seat_id(boarding_pass):
    row_range = [0, 127]
    col_range = [0, 7]
    return binary_search(row_range, boarding_pass[:7]) * 8 + binary_search(col_range, boarding_pass[7:])

# part 1
max_seat_id = 0

seat_id_list = []
with open('input.txt') as f:
    for line in f:
        boarding_pass = line.strip()

        pass_seat_id = seat_id(boarding_pass)
        if pass_seat_id > max_seat_id:
            max_seat_id = pass_seat_id

        seat_id_list.append(pass_seat_id)
print(max_seat_id)

# part 2
seat_id_list.sort()
for ii, pass_seat_id in enumerate(seat_id_list):
    if ii + seat_id_list[0] < pass_seat_id:
        print(ii + seat_id_list[0])
        break