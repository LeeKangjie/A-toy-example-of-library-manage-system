# -*- coding: utf-8 -*-
from utils import *

#define a function judge if a certain person can borrow a certain book, and reture a bool variables
def can_be_borrowed(books_out, person_name, book_name, days_requested, book_inventory, late_fees):
    available = False
    duplicate_book = False
    # Judge if this person already checked out this booked
    for book in books_out:
        if book[2] == book_name and book[1] == person_name:
            duplicate_book = True
    # Judge if this book important
    important = False
    for book in book_inventory:
        if book_name == book[0] and book[2]:
            important = True
    # Judge if this book being requested for too long
    too_long = False
    if important and days_requested > 7:
        too_long = True
    elif days_requested > 28:
        too_long = True
    if not too_long and not duplicate_book:
        # Does the borrower have too many late fees? ( > $50)
        too_many_fees = False
        for entry in late_fees:
            if person_name == entry[0] and entry[1] > 50:
                too_many_fees = True
        if not too_many_fees:
            for book in book_inventory:
                if book[0] == book_name and book[1] > 0:
                    available = True
    return available

#define a function judge if the person can return a certain book
def can_be_returned(person_name, book_name, books_out):
    returnable = False
    for entry in books_out:
        if entry[1] == person_name and entry[2] == book_name:
            returnable = True
    return returnable

# define a function calculating the usage: Usage = number of days borrowed / number of days available X 100
def calculate_usage(current_day, books_borrowed, original_books, added_books):
    # Calculating how many days was each book available
    book_usage = [] # the list format: [<book name>, <days avaliable>, <days borrowed>, <book_usage>]
    days_available = current_day - 1
    for book in original_books:
        book_usage.append([book[0], book[1] * days_available])
    for added_book in added_books:
        already_in_library = False
        for book in book_usage:
            if book[0] == added_book[0]:
                already_in_library = True
                book[1] += current_day - added_book[1]
        if not already_in_library:
            book_usage.append([added_book[0], (current_day - added_book[1])])
    # Calculating how many days was each book borrowed for
    for book in book_usage:
        book_was_borrowed = False
        for entry in books_borrowed:
            if book[0] == entry[0]:
                book.append(entry[1])
                book_was_borrowed = True
        if not book_was_borrowed:
            book.append(0)
    for book in book_usage:
        book.append(book[2] / book[1] * 100)
    book_usage.sort(key=lambda x: x[3], reverse=True)#sort in descend order
    for book in book_usage:
        print("\t- {} has a usage of {}%".format(book[0], round(book[3],2)))
    if len(book_usage) > 1:
        print("\nThe top used books are #1 {} and #2 {}".format(book_usage[0][0], book_usage[1][0]))

#this function is used to do the interract in the command line
def user_interface(current_day, books_borrowed, original_books, added_books, books_out, book_inventory, late_fees):
    leave = False
    while leave==False:
        print("Hi!  Please select an option:\n",
              "1) Can a person check out a certain book\n",
              "2) Can a person return a certain book\n",
              "3) Print list of peple with late fees\n",
              "4) Print the top used books\n",
              "5) Quit\n")
        option = int(input("Option #: "))
        if option == 1:
            print("Checking out a book")
            person_name = input("Person name: ")
            book_name = input("Book name: ")
            days_requested = int(input("For how many days? "))
            approved = can_be_borrowed(books_out, person_name, book_name, days_requested, book_inventory, late_fees)
            if approved:
                print("Yes! this book can be borrowed!")
            else:
                print("Sorry! This book cannot be borrowed")
        elif option == 2:
            print("Returning a book")
            person_name = input("Person name: ")
            book_name = input("Book name: ")
            if can_be_returned(person_name, book_name, books_out):
                print("Yes! This book can be returned")
            else:
                print("Sorry! This book cannot be returned")
        elif option == 3:
            print("Late fees:")
            for entry in late_fees:
                print("\t- {} has ${} of late fees".format(entry[0], entry[1]))
        elif option == 4:
            print("Usage Data:")
            calculate_usage(current_day, books_borrowed, original_books, added_books)
        elif option == 5:
            leave =True
        else:
            print("That is not a valid option.")



