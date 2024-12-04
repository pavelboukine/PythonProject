import csv
import matplotlib.pyplot as plt

# ======================= Persistence Layer =======================
class PipelineRecord:
    """
    Represents a single record from the pipeline dataset.
    
    Attributes:
    -----------
    throughput : str
        The throughput value of the pipeline.
    available_capacity : str
        The available capacity value of the pipeline.
    """

    def __init__(self, throughput, available_capacity):
        """
        Initializes a PipelineRecord object with throughput and available capacity.

        Parameters:
        -----------
        throughput : str
            The throughput value from the dataset.
        available_capacity : str
            The available capacity value from the dataset.
        """
        self.throughput = throughput
        self.available_capacity = available_capacity

    def __str__(self):
        """
        Returns a string representation of the PipelineRecord object.
        """
        return f"Throughput: {self.throughput} (1000 m3/d), Available Capacity: {self.available_capacity} (1000 m3/d)"
    
class FormattedPipelineRecord(PipelineRecord):
    """
    A subclass of PipelineRecord with a custom display format.
    Demonstrates inheritance by extending the functionality of the PipelineRecord class.
    
    Attributes:
    -----------
    Inherits all attributes from PipelineRecord:
    - throughput : str
        The throughput value of the pipeline.
    - available_capacity : str
        The available capacity value of the pipeline.
    """

    def __init__(self, throughput, available_capacity):
        """
        Initializes a FormattedPipelineRecord object with throughput and available capacity.

        Parameters:
        -----------
        throughput : str
            The throughput value from the dataset.
        available_capacity : str
            The available capacity value from the dataset.
        """
        # Call the superclass initializer
        super().__init__(throughput, available_capacity)

    def __str__(self):
        """
        Returns a custom string representation of the FormattedPipelineRecord object.

        Returns:
        --------
        str
            A fancy, formatted string representation of the record.
        """
        return (
            f"\n********** Formatted Pipeline Record **********\n"
            f"🚀 Throughput       : {self.throughput} (1000 m3/d)\n"
            f"💧 Available Capacity: {self.available_capacity} (1000 m3/d)\n"
            f"***********************************************"
        )


def load_data_from_file(file_name):
    """
    Loads up to 100 records from a CSV file and dynamically assigns record types.

    Parameters:
    -----------
    file_name : str
        The name of the CSV file to read from.

    Returns:
    --------
    list of PipelineRecord or FormattedPipelineRecord
        A list of record objects initialized from the dataset.
    """
    records = []
    try:
        with open(file_name, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Dynamically create FormattedPipelineRecord for high throughput
                if float(row['Throughput (1000 m3/d)']) > 50:
                    record = FormattedPipelineRecord(
                        row['Throughput (1000 m3/d)'],
                        row['Available Capacity (1000 m3/d)']
                    )
                else:
                    record = PipelineRecord(
                        row['Throughput (1000 m3/d)'],
                        row['Available Capacity (1000 m3/d)']
                    )
                records.append(record)
                if len(records) >= 100:
                    break
    except FileNotFoundError:
        print(f"Error: {file_name} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return records


def save_data_to_file(records, output_file):
    """
    Saves the in-memory data to a new CSV file.

    Parameters:
    -----------
    records : list of PipelineRecord
        The records to be saved to the CSV file.
    output_file : str
        The name of the output CSV file.
    """
    try:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Throughput (1000 m3/d)', 'Available Capacity (1000 m3/d)'])
            for record in records:
                writer.writerow([record.throughput, record.available_capacity])
        print(f"Data saved to {output_file} successfully.")
    except Exception as e:
        print(f"An error occurred while saving to {output_file}: {e}")

# ======================= Business Layer =======================
def add_record(records):
    """
    Adds a new PipelineRecord or FormattedPipelineRecord to the in-memory data.

    Parameters:
    -----------
    records : list of PipelineRecord
        The list to which the new record will be added.
    """
    throughput = input("Enter throughput (1000 m3/d): ")
    available_capacity = input("Enter available capacity (1000 m3/d): ")

    # Decide dynamically if the record should be formatted
    if float(throughput) > 50:
        record = FormattedPipelineRecord(throughput, available_capacity)
    else:
        record = PipelineRecord(throughput, available_capacity)

    records.append(record)
    print("Record added successfully.")

def edit_record(records):
    """
    Edits an existing record in the in-memory data.
    Re-evaluates the type of the record based on throughput after editing.

    Parameters:
    -----------
    records : list of PipelineRecord
        The list containing the records.
    """
    record_id = int(input(f"Enter record number to edit (1 to {len(records)}): ")) - 1
    if 0 <= record_id < len(records):
        current_record = records[record_id]
        throughput = input(f"Enter new throughput (current: {current_record.throughput}): ")
        available_capacity = input(f"Enter new available capacity (current: {current_record.available_capacity}): ")

        # Update the record
        current_record.throughput = throughput
        current_record.available_capacity = available_capacity

        # Re-evaluate the type of the record
        if float(throughput) > 50 and not isinstance(current_record, FormattedPipelineRecord):
            # Replace with FormattedPipelineRecord if conditions match
            records[record_id] = FormattedPipelineRecord(throughput, available_capacity)
            print("Record updated and converted to FormattedPipelineRecord.")
        elif float(throughput) <= 50 and isinstance(current_record, FormattedPipelineRecord):
            # Replace with PipelineRecord if conditions match
            records[record_id] = PipelineRecord(throughput, available_capacity)
            print("Record updated and converted to PipelineRecord.")
        else:
            print("Record updated successfully.")
    else:
        print("Invalid record number.")


def delete_record(records):
    """
    Deletes a record from the in-memory data.

    Parameters:
    -----------
    records : list of PipelineRecord
        The list containing the records.
    """
    record_id = int(input(f"Enter record number to delete (1 to {len(records)}): ")) - 1
    if 0 <= record_id < len(records):
        records.pop(record_id)
        print("Record deleted successfully.")
    else:
        print("Invalid record number.")

# ======================= Presentation Layer ========================
def display_records(records):
    """
    Displays all records in the dataset.

    Parameters:
    -----------
    records : list of PipelineRecord
        The list containing the records to be displayed.
    """
    print("\nPipeline Throughput and Capacity Records:")
    for i, record in enumerate(records):
        print(f"{i + 1}. {record}")

# ======================= New Feature: Horizontal Bar Chart =======================
def aggregate_data(records, field):
    """
    Aggregates records into categories based on selected field (capacity or throughput).

    Parameters:
    -----------
    records : list of PipelineRecord
        The list of records to aggregate.
    field : str
        The field to aggregate on, either 'available_capacity' or 'throughput'.

    Returns:
    --------
    dict
        A dictionary with categories as keys and counts as values.
    """
    categories = {"Low (0-20)": 0, "Medium (20-50)": 0, "High (50+)": 0}

    for record in records:
        value = float(getattr(record, field))
        if value <= 20:
            categories["Low (0-20)"] += 1
        elif 20 < value <= 50:
            categories["Medium (20-50)"] += 1
        else:
            categories["High (50+)"] += 1

    return categories


def generate_horizontal_bar_chart(records):
    """
    Generates a horizontal bar chart based on aggregated data categories.

    Parameters:
    -----------
    records : list of PipelineRecord
        The list of records to plot.
    """
    # Check if records are loaded
    if not records:
        print("\nNo data loaded. Please load data before generating a chart.")
        return

    # Ask the user to choose field
    print("\nChoose the field to visualize:")
    print("1. Available Capacity")
    print("2. Throughput")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        field = 'available_capacity'
        title = "Aggregated Horizontal Bar Chart: Available Capacity"
    elif choice == '2':
        field = 'throughput'
        title = "Aggregated Horizontal Bar Chart: Throughput"
    else:
        print("Invalid choice. Defaulting to Available Capacity.")
        field = 'available_capacity'
        title = "Aggregated Horizontal Bar Chart: Available Capacity"

    # Aggregate the data
    aggregated_data = aggregate_data(records, field)
    categories = list(aggregated_data.keys())
    counts = list(aggregated_data.values())

    # Create the bar chart
    plt.figure(figsize=(8, 6))
    plt.barh(categories, counts, color="skyblue")
    plt.xlabel("Number of Records")
    plt.ylabel("Categories")
    plt.title(title)
    plt.show()

# ======================= Menu =======================
def main_menu():
    """
    Displays the main menu and handles user input.
    """
    records = []
    file_name = 'keystone-throughput-and-capacity.csv'
    
    while True:
        print("\nMain Menu by Pavel Boukine")
        print("1. Load Data from CSV")
        print("2. Display Records")
        print("3. Add New Record")
        print("4. Edit a Record")
        print("5. Delete a Record")
        print("6. Save Data to New CSV")
        print("7. Plot Horizontal Bar Chart")  # New option
        print("8. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            records = load_data_from_file(file_name)
        elif choice == '2':
            if records:
                display_records(records)
            else:
                print("No records loaded.")
        elif choice == '3':
            add_record(records)
        elif choice == '4':
            if records:
                edit_record(records)
            else:
                print("No records loaded.")
        elif choice == '5':
            if records:
                delete_record(records)
            else:
                print("No records loaded.")
        elif choice == '6':
            output_file = input("Enter the name of the output file: ")
            save_data_to_file(records, output_file)
        elif choice == '7':  # New functionality
            generate_horizontal_bar_chart(records)
        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    print("Program by Pavel Boukine")
    main_menu()
