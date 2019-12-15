# -*- coding: utf-8 -*-
import copy#this package provides common shallow and deep copy operations

#define the function that could read the booklist from the txt format into list that could be operate in pyhton
def read_books_file():
    books = []#create a new black list
    books_file = open("booklargelist.txt", "r")#using the inline function open in read mode.
    book = books_file.readline()#read the text by line
    while book != "":#not the end of the line
        book = book.rstrip("\n")#delete linefeed in the end of the line
        book = book.split("#")#split the line using notation #
        book[1] = int(book[1])
        books.append(book)
        book = books_file.readline()
    books_file.close()#close the file
    return books

#define the checked_out function.
#return the booklist that nominally outside the librury:books_out
#return the booklist that still instored in the library:book_inventory
def checked_out(day, book_name, person_name, days, books_out, book_inventory):
    for book in book_inventory:
        if book[0] == book_name:
            book[1] -= 1
    books_out.append([day, person_name, book_name, days])
    return books_out, book_inventory

#define the late_fee function, documenting the person name and the corresponding fee for the late
def late_fee(current_day, day_borrowed, days_borrowed, book_name, person_name, fee_list, books):
    if current_day - days_borrowed > day_borrowed:  #judge if the book is late
        important = False
        already_fees = False
        days_late = current_day - day_borrowed - days_borrowed  #calculate how many days late is the book
        for book in books:
            if book[0] == book_name and book[2] == "True":  #judge if the book is important
                important = True
        if important:  # calculate the fee
            fee = days_late * 15
        else:
            fee = days_late * 5
        for entry in fee_list:  # Adds fee to fee_list
            if person_name == entry[0]:
                entry[1] += fee
                already_fees = True
        if not already_fees:
            fee_list.append([person_name, fee])
    return fee_list

#define the function that will be operated when a book is returned
#rerurn how many days a book borrowed in: books_borrowed
def returned(books_borrowed, current_day, book_name, person_name, books_out, fee_list, books):
    for book in books:
        if book[0] == book_name:
            book[1] += 1
    for entry in books_out:#searching in the books that outside the library
        if entry[1] == person_name and entry[2] == book_name:
            fee_list = late_fee(current_day, entry[3], entry[0], book_name, person_name, fee_list, books)# Check for fee
            already_in_borrowed = False# Update books_borrowed information
            for book in books_borrowed:
                if book[0] == book_name:
                    book[1] += (current_day - entry[0])
                    already_in_borrowed = True
            if not already_in_borrowed:
                books_borrowed.append([book_name, current_day - entry[0]])
            books_out.remove(entry)
    return books_borrowed, fee_list, books_out, books

#defien an operation when a new book is added in the library
#return the all books list and stored book list
def book_added(book_name, important, all_books, book_inventory):
    new_book = True
    for i in range(1,len(all_books)):
        if all_books[i][0] == book_name:
            new_book = False
            all_books[i][1] += 1  # add a copy to the library
            book_inventory[i][1] += 1  # add a copy to the library
    if new_book:
        all_books.append([book_name, 1, important])
        book_inventory.append([book_name, 1, important])
    return all_books, book_inventory

#updata the fee-list when a person has paied the fee
def payment_made(person_name, payment, fee_list):
    for entry in fee_list:
        if person_name == entry[0]:
            entry[1] -= payment
    return fee_list

#define a function that read the library activities
def read_log_file(book_inventory):
    all_books = copy.deepcopy(book_inventory)
    books_out = [] # the list format [<day checked out>, <person name>, <book name>, <days checked out for>]
    fee_list = []  # the list format [<person name>, <fee amount>]
    added_books = []  # the list format [<Book name>, <day_added>]
    books_borrowed = [] # the list format [<Book name>, <# of days borrowed>]
    current_day = 0
    log_file = open("libraryloglarge.txt", "r")#the grammer is same as read_books_file()
    log = log_file.readline()
    while log != "":
        log = log.rstrip("\n")
        log = log.split("#")
        if len(log) == 1:# End date
            current_day = int(log[0])
        elif len(log) == 3:# Book was added to the library
            all_books, book_inventory = book_added((log[1]), log[2], all_books, book_inventory)#call the book_added defined above
            added_books.append([log[1], int(log[0])])
        elif log[0] == "PAY":# Payment was made
            fee_list = payment_made(log[2], int(log[3]), fee_list)#call the payment_made defined above
        elif log[3] == "RET":# Book was returned
            books_borrowed, fee_list, books_out, book_inventory = returned(books_borrowed, int(log[0]), log[1], log[2],
                                                                           books_out, fee_list, book_inventory)#call the returned function defined above
        else:# Book was checked out
            books_out, book_inventory = checked_out(int(log[0]), log[1], log[2], int(log[3]), books_out, book_inventory)#call the check_out function defined above
        log = log_file.readline()
    log_file.close()

    # Update books borrowed
    already_borrowed = False
    for entry in books_out:
        for book in books_borrowed:#
            if entry[2] == book[0]:
                book[1] += (current_day - entry[0])
                already_borrowed = True
        if not already_borrowed:
            books_borrowed.append([entry[2], current_day - entry[0]])

    # Update late fees for books still out
    for entry in books_out:
        fee_list = late_fee(current_day, entry[0], entry[3], entry[2], entry[1], fee_list, book_inventory)
    return books_borrowed, added_books, current_day, fee_list, books_out, all_books, book_inventory


