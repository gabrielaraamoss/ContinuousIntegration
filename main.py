import datetime

class Book:
    def __init__(self, title, author, quantity):
        self.title = title
        self.author = author
        self.quantity_available = quantity
        self.checked_out = 0

class Library:
    def __init__(self):
        self.books = [
            Book("Book1", "Author1", 5),
            Book("Book2", "Author2", 3),
            Book("Book3", "Author3", 8)
            # Add more books as needed
        ]
        self.checked_out_books = []

    def display_catalog(self):
        print("Catalog:")
        for idx, book in enumerate(self.books):
            print(f"{idx + 1}. {book.title} by {book.author} - Available: {book.quantity_available}")

    def validate_quantity(self, quantity_str):
        try:
            quantity = int(quantity_str)
            if quantity > 0:
                return quantity
            else:
                raise ValueError("Quantity must be a positive integer.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            return -1

    def checkout_books(self, selections):
        total_late_fees = 0
        for selection in selections:
            book = self.books[selection["book_index"]]
            quantity = selection["quantity"]
            if book.quantity_available >= quantity:
                book.quantity_available -= quantity
                book.checked_out += quantity
                due_date = datetime.datetime.now() + datetime.timedelta(days=14)
                selection["due_date"] = due_date
                late_fees = self.calculate_late_fees(due_date)
                total_late_fees += late_fees
            else:
                print(f"Error: Insufficient quantity of {book.title} available.")
                return -1
        self.checked_out_books.extend(selections)
        return total_late_fees

    def calculate_late_fees(self, due_date):
        today = datetime.datetime.now()
        if today > due_date:
            days_overdue = (today - due_date).days
            return days_overdue
        return 0

    def display_checkout_summary(self, selections, total_late_fees):
        print("\nCheckout Summary:")
        for selection in selections:
            book = self.books[selection["book_index"]]
            print(f"{book.title} (Quantity: {selection['quantity']}) - Due Date: {selection['due_date'].strftime('%Y-%m-%d')}")
        print(f"\nTotal Late Fees: ${total_late_fees:.2f}")

    def return_books(self, return_details):
        total_late_fees = 0
        for return_detail in return_details:
            book = self.books[return_detail["book_index"]]
            quantity_returned = return_detail["quantity"]
            if book.checked_out >= quantity_returned:
                book.checked_out -= quantity_returned
                return_date = datetime.datetime.now()
                late_fees = self.calculate_late_fees(return_detail["due_date"])
                total_late_fees += late_fees
            else:
                print(f"Error: Invalid quantity returned for {book.title}.")
                return -1
        return total_late_fees

    def display_return_summary(self, return_details, total_late_fees):
        print("\nReturn Summary:")
        for return_detail in return_details:
            book = self.books[return_detail["book_index"]]
            print(f"{book.title} (Quantity Returned: {return_detail['quantity']}) - Late Fees: ${total_late_fees:.2f}")


def main():
    library = Library()

    while True:
        print("\n1. Display Catalog\n2. Checkout Books\n3. Return Books\n4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            library.display_catalog()
        elif choice == "2":
            selections = []
            while True:
                library.display_catalog()
                book_index_str = input("Enter the index of the book to checkout (0 to finish): ")
                if book_index_str == "0":
                    break

                book_index = library.validate_quantity(book_index_str)
                if book_index != -1 and 0 <= book_index < len(library.books):
                    quantity_str = input("Enter the quantity: ")
                    quantity = library.validate_quantity(quantity_str)
                    if quantity != -1 and quantity <= 10:
                        selections.append({"book_index": book_index, "quantity": quantity})
                    elif quantity > 10:
                        print("Error: Maximum 10 books allowed per checkout.")
                    else:
                        print("Invalid quantity. Please try again.")

            total_late_fees = library.checkout_books(selections)
            if total_late_fees != -1:
                library.display_checkout_summary(selections, total_late_fees)

        elif choice == "3":
            return_details = []
            while True:
                library.display_catalog()
                book_index_str = input("Enter the index of the book to return (0 to finish): ")
                if book_index_str == "0":
                    break

                book_index = library.validate_quantity(book_index_str)
                if book_index != -1 and 0 <= book_index < len(library.books):
                    quantity_str = input("Enter the quantity to return: ")
                    quantity_returned = library.validate_quantity(quantity_str)
                    if quantity_returned != -1:
                        selection = {"book_index": book_index, "quantity": quantity_returned,
                                      "due_date": datetime.datetime.now()}
                        return_details.append(selection)
                    else:
                        print("Invalid quantity. Please try again.")

            total_late_fees = library.return_books(return_details)
            if total_late_fees != -1:
                library.display_return_summary(return_details, total_late_fees)

        elif choice == "4":
            print("Exiting the Library Book Checkout System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
