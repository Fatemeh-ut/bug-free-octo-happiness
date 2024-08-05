import pythonscript as pt
import time


def main():
    user = None
    print(f"----- wellcome to our library -----\n")

    while True:
        log_sign = input("log in or sign in(enter l or s) : ")
        log_sign = log_sign.lower()
        match log_sign:
            case "l":
                userName = input("Enter your username : ")
                password = input("Enter your password : ")
                user = pt.Database.login(pt.hash_code(userName), pt.hash_code(password),"u")
                admin = pt.Database.login(pt.hash_code(userName), pt.hash_code(password), "a")
                if user is not None:
                    print(f"welcome back *{user.get_first_name()} {user.get_last_name()}* \n")
                    break
                elif admin is not None:
                    print(f"Hello amin *{admin.get_first_name()} {admin.get_last_name()}* ")
                    break
                else:
                    print("Invalid username or password")
            case "s":
                firstName = input("Enter your first name : ")
                lastName = input("Enter your last name : ")
                while True:
                    userName = input("Enter your username : ")
                    if pt.Database.unique_username(pt.hash_code(userName), "user"):
                        print("Please enter am unique username")
                    else:
                        break
                password = input("Enter your password : ")
                while True:
                    password2 = input("Enter your password again : ")
                    if password == password2:
                        user = pt.User(pt.hash_code(firstName), pt.hash_code(lastName), pt.hash_code(userName),
                                       pt.hash_code(password), "")
                        pt.Database.signin(user)
                        break

                    else:
                        print("Passwords do not match")
            case _:
                log_sign = input("log in or sign in(enter l or s) : ")
    time.sleep(1)
    while True and user is not None:
        action = input('Enter action'
                       '[ delete -> for delete account \n'
                       'make -> for make a reservation \n'
                       'show -> for reservations made (and deleting them) ] '
                       'action : ')

        match action:
            case "delete":
                act = input('Are you sure to delete account ?(y / N) :')
                match act:
                    case 'y':
                        pt.Database.delete_user(user)
                        print("Deleted successfully")
                        break
                    case 'N':
                        action = input('Enter action'
                                       '[ delete -> for delete account \n'
                                       'make -> for make a reservation \n'
                                       'show -> for reservations made (and deleting them) ]'
                                       'action : ')

            case "make":
                pt.Database.show_reserve()
                while True:
                    act = input('For make reservation please enter [id:time1, time2 or time3]\n (for quite enter q): ')
                    match act:
                        case 'q' | 'Q':
                            print('reservations is done!\n')
                            break
                        case _:
                            if ":" in act:
                                if not pt.Database.make_reservation(act, user):
                                    print("id doesn't exist\n")
                break

            case "show":
                print("----- your profile -----")
                print(user.__str__())
                print("----- your reservation -----")
                list_num = user.get_reservations()
                while True:
                    act = (input('Enter the number for deleting reservations (for quite enter q) : '))
                    if act == 'q' or act == 'Q':
                        break
                    elif int(act) in list_num:
                        user.delete_reservation(int(act))
                        print("Deleted successfully")
                        break
                    else:
                        act = input('Enter the number for deleting reservations (for quite enter q) : ')
                break
            case _:
                action = input('Enter action'
                               '[ delete -> for delete account \n'
                               'make -> for make a reservation \n'
                               'show -> for reservations made (and deleting them) ]'
                               'action : ')
    while True and admin is not None:
        action = input("Enter action"
                       "[add -> for add a new Admin \n"
                       "report -> to get the report (for quit q)] : ")
        match action:
            case "add":
                firstName = input("Enter your first name : ")
                lastName = input("Enter your last name : ")
                while True:
                    userName = input("Enter your username : ")
                    if pt.Database.unique_username(pt.hash_code(userName), "admins"):
                        print("Please enter am unique username")
                    else:
                        break
                password = input("Enter your password : ")
                while True:
                    password2 = input("Enter your password again : ")
                    if password == password2:
                        new_admin = pt.Admin(pt.hash_code(firstName), pt.hash_code(lastName), pt.hash_code(userName), pt.hash_code(password))
                        pt.Admin.add_admin(new_admin)
                        break
                    else:
                        print("Passwords do not match")
            case "report":
                print("----- date ----- time1---time2---time3")
                pt.Admin.get_report()
                pt.Admin.most_reservation()
                while True:
                    act = input("Enter action \n"
                                "[delete -> passed times\n"
                                "add -> to add reservations for the next 7 dat]  \n : ")
                    match act:
                        case "add":
                            pt.Admin.add_new_reserve()
                            print("Added successfully")
                            break
                        case "delete":
                            pt.Admin.delete_pass()
                            print("Deleted successfully")
                            break
                        case _:
                            act = input("Enter action \n"
                                        "[delete -> passed times\n"
                                        "add -> to add reservations for the next 7 dat]  \n : ")

            case "q" | 'Q':
                break
            case _:
                action = input("Enter action"
                               "[add -> for add a new Admin \n"
                               "report -> to get the report (for quit q)] \n")


if __name__ == "__main__":
    main()
