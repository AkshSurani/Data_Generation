import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta, date
import json
# import uuid
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Initialize Faker
fake = Faker('en_IN')  # Using Indian locale

# Create output directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Define number of records to generate
# num_records = 100

## LOCATIONS
NUM_LOCATIONS = 50  # Number of locations
LOCATION_START_ID = 1
LOCATION_END_ID = LOCATION_START_ID + NUM_LOCATIONS

## RESTAURANTS
NUM_RESTAURANTS = 100  # Number of restaurants (increased to have restaurants in multiple cities)
RESTAURANT_START_ID = 1
RESTAURANT_END_ID = RESTAURANT_START_ID + NUM_RESTAURANTS

## MENU
NUM_MENU = 500  # Number of menu items
MENU_START_ID = 1
MENU_END_ID = MENU_START_ID + NUM_MENU

## CUSTOMERS
NUM_CUSTOMERS = 2000  # Number of customers
CUSTOMER_START_ID = 1
CUSTOMER_END_ID = CUSTOMER_START_ID + NUM_CUSTOMERS

## CUSTOMER ADDRESS - Multiple addresses per customer
NUM_CUSTOMER_ADDRESS = 00
CUSTOMER_ADDRESS_START_ID = 1
CUSTOMER_ADDRESS_END_ID = CUSTOMER_ADDRESS_START_ID + NUM_CUSTOMER_ADDRESS

## CUSTOMER LOGIN AUDIT
NUM_CUSTOMER_LOGIN_AUDIT = NUM_CUSTOMERS * 5
CUSTOMER_LOGIN_AUDIT_START_ID = 1
CUSTOMER_LOGIN_AUDIT_END_ID = CUSTOMER_LOGIN_AUDIT_START_ID + NUM_CUSTOMER_LOGIN_AUDIT

## ORDERS
NUM_ORDERS = 100  # Number of orders
ORDER_START_ID = 1
ORDER_END_ID = ORDER_START_ID + NUM_ORDERS

DELIVERY_START_ID = 1

## DELIVERY AGENTS - Distributed across locations
NUM_DELIVERY_AGENT = 150
DELIVERY_AGENT_START_ID = 1
DELIVERY_AGENT_END_ID= DELIVERY_AGENT_START_ID + NUM_DELIVERY_AGENT

## CURRENT DATE FOR FILE SAVE 
CURRENT_DATE = datetime.now()


def generate_location_data(location_start_id, location_end_id):
    # Indian cities and states
    cities_states = [
        ('Delhi', 'Delhi'),
        ('Mumbai', 'Maharashtra'),
        ('Bangalore', 'Karnataka'),
        ('Hyderabad', 'Telangana'),
        ('Chennai', 'Tamil Nadu'),
        ('Kolkata', 'West Bengal'),
        ('Pune', 'Maharashtra'),
        ('Ahmedabad', 'Gujarat'),
        ('Jaipur', 'Rajasthan'),
        ('Lucknow', 'Uttar Pradesh'),
        ('Chandigarh', 'Punjab'),
        ('Bhopal', 'Madhya Pradesh'),
        ('Guwahati', 'Assam'),
        ('Kochi', 'Kerala'),
        ('Indore', 'Madhya Pradesh'),
        ('Surat', 'Gujarat'),
        ('Nagpur', 'Maharashtra'),
        ('Patna', 'Bihar'),
        ('Vadodara', 'Gujarat'),
        ('Thane', 'Maharashtra'),
        ('Agra', 'Uttar Pradesh'),
        ('Nashik', 'Maharashtra'),
        ('Faridabad', 'Haryana'),
        ('Meerut', 'Uttar Pradesh'),
        ('Rajkot', 'Gujarat'),
        ('Varanasi', 'Uttar Pradesh'),
        ('Srinagar', 'Jammu and Kashmir'),
        ('Aurangabad', 'Maharashtra'),
        ('Dhanbad', 'Jharkhand'),
        ('Amritsar', 'Punjab')
    ]
    
    data = []
    location_id = location_start_id
    for city, state in cities_states:
        zipcode = f"{random.randint(110000, 999999)}"
        active_flag = np.random.choice(['Yes', 'No'], p=[0.90, 0.1])
        created_date = fake.date_time_between(start_date='-3y', end_date='now')
        modified_date = fake.date_time_between(start_date=created_date, end_date='now') if random.random() > 0.3 else None
        
        data.append({
            'LocationID': location_id,
            'City': city,
            'State': state,
            'ZipCode': zipcode,
            'ActiveFlag': active_flag,
            'CreatedDate': created_date,
            'ModifiedDate': modified_date
        })
        location_id += 1
        
        # if location_id >= location_end_id:
            # break
    
    return pd.DataFrame(data)


def generate_restaurant_data(restaurant_start_id, restaurant_end_id, location_df):
    # Cuisine types
    cuisine_types = [
        "North Indian", "South Indian", "Chinese", "Italian", "Continental", 
        "Mediterranean", "Mexican", "Thai", "Japanese", "Lebanese", 
        "Mughlai", "Street Food", "Desserts", "Beverages", "Fast Food",
        "Cafe", "Bakery", "Ice Cream", "Pizza", "Burger"
    ]
    
    # Restaurant names
    first_parts = ["Royal", "Spice", "Taste", "Flavors", "Urban", "Green", "Blue", "Red", 
                  "Golden", "Silver", "Diamond", "Emerald", "Crystal", "Pearl", "Ruby"]
    second_parts = ["Kitchen", "Bistro", "Restaurant", "Cafe", "Diner", "Eatery", "Grill", 
                   "Bites", "Table", "Garden", "House", "Palace", "Corner", "Junction", "Hub"]
    
    data = []
    # Get only active locations
    active_locations = location_df[location_df['ActiveFlag'] == 'Yes']
    
    # Distribute restaurants across all active locations
    restaurant_id = restaurant_start_id
    
    # Ensure each location has at least 2-5 restaurants
    for _, location_row in active_locations.iterrows():
        location_id = location_row['LocationID']
        city_name = location_row['City']
        
        # Create 2-5 restaurants per location
        num_restaurants_for_location = random.randint(20, 50)
        
        for _ in range(num_restaurants_for_location):
            # Generate restaurant name
            name = f"{random.choice(first_parts)} {random.choice(second_parts)}"
            
            # Generate cuisine types (1-3 random cuisine types)
            num_cuisines = random.randint(1, 3)
            restaurant_cuisines = random.sample(cuisine_types, num_cuisines)
            cuisine_type = ", ".join(restaurant_cuisines)
            
            # Other fields
            pricing_for_2 = random.randint(200, 2000)
            phone = f"9{random.randint(100000000, 999999999)}"
            
            # Opening and closing hours
            opening_hour = random.randint(7, 12)
            closing_hour = random.randint(17, 23)
            operating_hours = f"{opening_hour}:00 AM - {closing_hour}:00 PM"
            
            active_flag = np.random.choice(['Yes', 'No'], p=[0.9, 0.1])
            open_status = 'Open' if active_flag == 'Yes' else 'Closed'
    
            # Address and locality
            locality = f"{fake.street_name()}"
            city_pincode = location_row['ZipCode']
            restaurant_address = f'{random.choice(["Ground Floor,","First Floor,","Second Floor,","Third Floor,", ""])} {locality}, {city_name} - {city_pincode}'
            
            # Coordinates (latitude and longitude for India)
            latitude = random.uniform(8.4, 37.6)
            longitude = random.uniform(68.7, 97.25)
            
            # Dates
            created_date = fake.date_time_between(start_date='-3y', end_date='-1y')
            modified_date = fake.date_time_between(start_date=created_date, end_date='now')
            
            data.append({
                'RestaurantID': restaurant_id,
                'Name': name,
                'CuisineType': cuisine_type,
                'Pricing_for_2': pricing_for_2,
                'Restaurant_Phone': phone,
                'OperatingHours': operating_hours,
                'LocationID': location_id,
                'ActiveFlag': active_flag,
                'OpenStatus': open_status,
                'Locality': locality,
                'Restaurant_Address': restaurant_address,
                'Latitude': latitude,
                'Longitude': longitude,
                'CreatedDate': created_date,
                'ModifiedDate': modified_date
            })
            
            restaurant_id += 1
            # if restaurant_id >= restaurant_end_id:
            #     break
                
        # if restaurant_id >= restaurant_end_id:
        #     break
    
    # If we still have room for more restaurants, continue adding them to random locations
    # while restaurant_id < restaurant_end_id:
    #     location_id = random.choice(active_locations['LocationID'])
    #     city_name = active_locations[active_locations['LocationID'] == location_id]['City'].values[0]
        
    #     # Generate restaurant name
    #     name = f"{random.choice(first_parts)} {random.choice(second_parts)}"
        
    #     # Generate cuisine types
    #     num_cuisines = random.randint(1, 3)
    #     restaurant_cuisines = random.sample(cuisine_types, num_cuisines)
    #     cuisine_type = ", ".join(restaurant_cuisines)
        
    #     # Other fields
    #     pricing_for_2 = random.randint(200, 2000)
    #     phone = f"9{random.randint(100000000, 999999999)}"
        
    #     # Operating hours
    #     opening_hour = random.randint(7, 12)
    #     closing_hour = random.randint(17, 23)
    #     operating_hours = f"{opening_hour}:00 AM - {closing_hour}:00 PM"
        
    #     active_flag = np.random.choice(['Yes', 'No'], p=[0.9, 0.1])
    #     open_status = 'Open' if active_flag == 'Yes' else 'Closed'

    #     # Address
    #     locality = f"{fake.street_name()}"
    #     city_pincode = active_locations[active_locations['LocationID'] == location_id]['ZipCode'].values[0]
    #     restaurant_address = f'{random.choice(["Ground Floor,","First Floor,","Second Floor,","Third Floor,", ""])} {locality}, {city_name} - {city_pincode}'
        
    #     # Coordinates
    #     latitude = random.uniform(8.4, 37.6)
    #     longitude = random.uniform(68.7, 97.25)
        
    #     # Dates
    #     created_date = fake.date_time_between(start_date='-3y', end_date='-1y')
    #     modified_date = fake.date_time_between(start_date=created_date, end_date='now')
        
    #     data.append({
    #         'RestaurantID': restaurant_id,
    #         'Name': name,
    #         'CuisineType': cuisine_type,
    #         'Pricing_for_2': pricing_for_2,
    #         'Restaurant_Phone': phone,
    #         'OperatingHours': operating_hours,
    #         'LocationID': location_id,
    #         'ActiveFlag': active_flag,
    #         'OpenStatus': open_status,
    #         'Locality': locality,
    #         'Restaurant_Address': restaurant_address,
    #         'Latitude': latitude,
    #         'Longitude': longitude,
    #         'CreatedDate': created_date,
    #         'ModifiedDate': modified_date
    #     })
        
    #     restaurant_id += 1
    
    return pd.DataFrame(data)


def generate_menu_data(menu_start_id, menu_end_id, restaurant_df):
    categories = ["Appetizers", "Main Course", "Desserts", "Beverages", "Snacks"]
    item_names = {
        "Appetizers": ["Samosa", "Paneer Tikka", "Chicken Tikka", "Aloo Tikki", "Fish Fry", "Spring Rolls", "Hara Bhara Kebab", "Seekh Kebab", "Chicken Wings", "Prawn Skewers"],
        "Main Course": ["Butter Chicken", "Paneer Butter Masala", "Dal Makhani", "Chole Bhature", "Biryani", "Rogan Josh", "Palak Paneer", "Malai Kofta", "Mutton Curry", "Fish Curry"],
        "Desserts": ["Gulab Jamun", "Rasgulla", "Kheer", "Jalebi", "Kulfi", "Ras Malai", "Gajar Halwa", "Mysore Pak", "Peda", "Sandesh"],
        "Beverages": ["Masala Chai", "Lassi", "Nimbu Pani", "Cold Coffee", "Fruit Juice", "Coconut Water", "Aam Panna", "Buttermilk", "Thandai", "Falooda"],
        "Snacks": ["Pav Bhaji", "Bhel Puri", "Pani Puri", "Vada Pav", "Pakora", "Dhokla", "Kachori", "Sev Puri", "Dabeli", "Aloo Chaat"]
    }
    descriptions = ["Delicious and authentic {}.", "A popular Indian dish.", "Traditional Indian {} with rich flavors.", "A must-try {} from India.", "Classic {} with a twist."]
    
    data = []
    menu_id = menu_start_id
    
    # Ensure each restaurant has at least a few menu items
    for restaurant_id in restaurant_df['RestaurantID']:
        # Create 3-10 menu items per restaurant
        num_items = random.randint(10, 15)
        
        # Create a set to track what items we've already added to this restaurant
        restaurant_items = set()
        
        for _ in range(num_items):
            category = random.choice(categories)
            
            # Try to find an item name not already in use for this restaurant
            attempts = 0
            while attempts < 20:  # Prevent infinite loop
                item_name = random.choice(item_names[category])
                if item_name not in restaurant_items:
                    restaurant_items.add(item_name)
                    break
                attempts += 1
            
            if attempts >= 20:
                # Just pick any item if we can't find a unique one
                item_name = random.choice(item_names[category])
            
            # Set item type based on item name
            if item_name in ["Chicken Tikka", "Fish Fry", "Seekh Kebab", "Chicken Wings", 
                             "Prawn Skewers", "Butter Chicken", "Biryani", "Rogan Josh", 
                             "Mutton Curry", "Fish Curry"]:
                item_type = "Non-Veg"
            else:
                item_type = "Veg"
            
            description = random.choice(descriptions).format(item_name)
            price = random.randint(50, 500)
            created_date = fake.date_time_between(start_date='-3y', end_date='-1y')
            modified_date = fake.date_time_between(start_date=created_date, end_date='now')

            data.append({
                "MenuID": menu_id,
                "RestaurantID": restaurant_id,
                "ItemName": item_name,
                "Description": description,
                "Price": price,
                "Category": category,
                "Availability": True,
                "ItemType": item_type,
                "CreatedDate": created_date,
                "ModifiedDate": modified_date
            })
            
            menu_id += 1
            # if menu_id >= menu_end_id:
            #     break
                
        # if menu_id >= menu_end_id:
        #     break
    
    return pd.DataFrame(data)


def generate_customer_data(customer_start_id, customer_end_id):
    login_methods = ['GMail_Account', 'Apple_ID', 'Other_EMail']
    genders = ['Male', 'Female', 'Other']
    
    food_preferences = ['Veg', 'Non-Veg', 'Vegan', 'Eggetarian']
    cuisine_types = ['North Indian', 'South Indian', 'Chinese', 'Italian', 'Continental', 
                      'Mediterranean', 'Mexican', 'Thai', 'Japanese', 'Street Food']
    
    data = []
    for i in range(customer_start_id, customer_end_id):
        # Basic info
        gender = random.choice(genders)
        if gender == 'Male':
            name = fake.name_male()
        elif gender == 'Female':
            name = fake.name_female()
        else:
            name = fake.name()
            
        mobile = f"{random.randint(7000000000, 9999999999)}"
        email_domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])
        email = f"{name.lower().replace(' ', '')}{random.randint(1, 999)}@{email_domain}"
        login_using = random.choice(login_methods)
        
        # Generate random birth date (18-60 years old)
        dob = fake.date_of_birth(minimum_age=15, maximum_age=75)
        
        # Generate anniversary date (0-30 years after birth date)
        years_after_dob = random.randint(18, 30)  # Most people marry after 21
        anniversary = dob + timedelta(days=365 * years_after_dob)
        
        # Check if anniversary is in the future
        anniversary = anniversary if anniversary < datetime.date(datetime.now()) else None
        anniversary = np.random.choice([anniversary, None], p=[0.7, 0.3])

        # Generate food preferences
        food_pref = random.choice(food_preferences)
        num_cuisines = random.randint(1, 5)
        cuisine_pref = random.sample(cuisine_types, num_cuisines)
        
        preferences = {
            'FoodPreference': food_pref,
            'CuisineTypes': cuisine_pref
        }
        
        # Dates
        created_date = fake.date_time_between(start_date='-3y', end_date='-1m')
        modified_date = fake.date_time_between(start_date=created_date, end_date='now')

        data.append({
            'CustomerID': i,
            # 'Name': name,
            # 'Mobile': mobile,
            # 'Email': email,
            # 'LoginByUsing': login_using,
            # 'Gender': gender,
            # 'DOB': dob,
            # 'Anniversary': anniversary,
            'Preferences1': preferences,
            'Preferences': json.dumps(preferences),
            # 'CreatedDate': created_date,
            # 'ModifiedDate': modified_date
        })
    
    return pd.DataFrame(data)


def generate_customer_address_data(customer_address_start_id, customer_address_end_id, customer_df, location_df):
    address_types = ['Home', 'Work', 'Other']
    
    data = []
    address_id = customer_address_start_id
    
    # Get active locations for address assignment
    active_locations = location_df[location_df['ActiveFlag'] == 'Yes']
    
    # Generate 1-4 addresses per customer in different cities
    for customer_id in customer_df['CustomerID']:
        # Number of addresses for this customer
        num_addresses = random.randint(1, 4)
        
        # Randomly select locations for this customer
        customer_locations = active_locations.sample(min(num_addresses, len(active_locations)))
        
        for idx, location_row in enumerate(customer_locations.iterrows()):
            location_data = location_row[1]  # Get the Series from the tuple
            location_id = location_data['LocationID']
            city = location_data['City']
            state = location_data['State']
            pincode = location_data['ZipCode']
            
            flat_no = str(random.randint(1, 50))
            # house_no = str(random.randint(1, 10)) if random.random() > 0.5 else ""
            floor = str(random.randint(1, 40)) if random.random() > 0.3 else ""
            building = fake.company() + " " + random.choice(['Apartments', 'Residency', 'Heights', 'Towers', 'Complex'])
            landmark = random.choice(["Near ","Opp. ","B/h. ","Beside ","Behind ",""]) + fake.company()
            
            # Locality
            locality =  locality = random.choice([
                'Saket', 'Connaught Place', 'Dwarka', 'Vasant Kunj', 'South Extension',
                'Rohini', 'Karol Bagh', 'Pitampura', 'Janakpuri', 'Lajpat Nagar',
                'Malviya Nagar', 'Greater Kailash', 'Hauz Khas', 'Mayur Vihar', 'Rajouri Garden'
            ])
            
            # Coordinates
            latitude = random.uniform(8.4, 37.6)
            longitude = random.uniform(68.7, 97.25)
            coordinates = f"{latitude},{longitude}"
            
            # Primary flag (only one primary address per customer)
            primary_flag = "Yes" if idx == 0 else "No"
            address_type = random.choice(address_types)
            
            # Dates
            customer_created_date = customer_df[customer_df['CustomerID'] == customer_id]['CreatedDate'].values[0]
            created_date = fake.date_time_between(start_date=pd.to_datetime(customer_created_date), end_date='now')
            modified_date = fake.date_time_between(start_date=created_date, end_date='now') if random.random() > 0.3 else None

            data.append({
                'AddressID': address_id,
                'CustomerID': customer_id,
                'FlatNo/HouseNo': flat_no,
                'Floor': floor,
                'Building': building,
                'Landmark': landmark,
                'Locality': locality,
                'City': city,
                'State': state,
                'Pincode': pincode,
                'Coordinates': coordinates,
                'PrimaryFlag': primary_flag,
                'AddressType': address_type,
                'CreatedDate': created_date,
                'ModifiedDate': modified_date,
                'LocationID': location_id  # Adding this temporarily to link addresses to locations
            })
            
            address_id += 1
            
    
    result_df = pd.DataFrame(data)
    
    # Remove the temporary LocationID column before returning
    # if 'LocationID' in result_df.columns:
    #     return result_df.drop(columns=['LocationID'])
    return result_df


def generate_login_audit_data(customer_login_audit_start_id, customer_login_audit_end_id, customer_df):
    login_types = ['App', 'Web']
    device_interfaces = ['Android', 'iOS']
    mobile_devices = ['Samsung Galaxy', 'OnePlus', 'Xiaomi', 'Oppo', 'Vivo', 'Realme']
    web_interfaces = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
    
    data = []
    for i in range(customer_login_audit_start_id, customer_login_audit_end_id):
        # Random customer
        customer_id = random.choice(customer_df['CustomerID'])
        
        # Login details
        login_type = np.random.choice(login_types, p=[0.9, 0.1])
        
        # Device details depend on login type
        if login_type == 'App':
            device_interface = np.random.choice(device_interfaces, p=[0.7, 0.3])
            mobile_device_name = 'iPhone' if device_interface=='iOS' else random.choice(mobile_devices)
            web_interface = None
        else:  # Web or Desktop
            device_interface = None
            mobile_device_name = None
            web_interface = random.choice(web_interfaces)
        
        # Login timestamp
        last_login = fake.date_time_between(start_date='-3y', end_date='now')
        
        data.append({
            'LoginID': i,
            'CustomerID': customer_id,
            'LoginType': login_type,
            'DeviceInterface': device_interface,
            'MobileDeviceName': mobile_device_name,
            'WebInterface': web_interface,
            'LastLogin': last_login
        })
    
    return pd.DataFrame(data)


def generate_delivery_agent_data(delivery_agents_start_id, delivery_agent_end_id, location_df):
    vehicle_types = ['Bike', 'Scooter']
    
    data = []
    
    # Ensure each active location has at least 2-5 delivery agents
    active_locations = location_df[location_df['ActiveFlag'] == 'Yes']
    delivery_agent_id = delivery_agents_start_id
    
    for _, location_row in active_locations.iterrows():
        location_id = location_row['LocationID']
        
        # Number of agents for this location
        num_agents = random.randint(50, 100)
        
        for _ in range(num_agents):
            # Basic info
            gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.9, 0.09, 0.01])
            
            if gender == 'Male':
                name = fake.name_male()
            elif gender == 'Female':
                name = fake.name_female()
            else:
                name = fake.name()
                
            phone = f"{random.randint(7000000000, 9999999999)}"
            vehicle_type = random.choice(vehicle_types)
            status = np.random.choice(['Active', 'Inactive'], p=[0.9, 0.1])
            
            # Rating (1.0 to 5.0)
            rating = round(random.uniform(3.0, 5.0), 1)
            
            # Dates
            created_date = fake.date_time_between(start_date='-2y', end_date='-3m')
            modified_date = fake.date_time_between(start_date=created_date, end_date='now')
            
            data.append({
                'DeliveryAgentID': delivery_agent_id,
                'Name': name,
                'Phone': phone,
                'VehicleType': vehicle_type,
                'LocationID': location_id,
                'Status': status,
                'Gender': gender,
                'Rating': rating,
                'CreatedDate': created_date,
                'ModifiedDate': modified_date
            })
            
            delivery_agent_id += 1
        #     if delivery_agent_id >= delivery_agent_end_id:
        #         break
                
        # if delivery_agent_id >= delivery_agent_end_id:
        #     break
    
    # If needed, add more agents to random locations
    # while delivery_agent_id < delivery_agent_end_id:
    #     location_id = random.choice(active_locations['LocationID'])
        
    #     gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.9, 0.09, 0.01])
    #     if gender == 'Male':
    #         name = fake.name_male()
    #     elif gender == 'Female':
    #         name = fake.name_female()
    #     else:
    #         name = fake.name()
            
    #     phone = f"{random.randint(7000000000, 9999999999)}"
    #     vehicle_type = random.choice(vehicle_types)
    #     status = np.random.choice(['Active', 'Inactive'], p=[0.9, 0.1])
        
    #     # Rating (1.0 to 5.0)
    #     rating = round(random.uniform(3.0, 5.0), 1)
        
    #     # Dates
    #     created_date = fake.date_time_between(start_date='-2y', end_date='-3m')
    #     modified_date = fake.date_time_between(start_date=created_date, end_date='now')
        
    #     data.append({
    #         'DeliveryAgentID': delivery_agent_id,
    #         'Name': name,
    #         'Phone': phone,
    #         'VehicleType': vehicle_type,
    #         'LocationID': location_id,
    #         'Status': status,
    #         'Gender': gender,
    #         'Rating': rating,
    #         'CreatedDate': created_date,
    #         'ModifiedDate': modified_date
    #     })
        
    #     delivery_agent_id += 1
    
    return pd.DataFrame(data)

def generate_orders_data(order_start_id, order_end_id, customer_df, restaurant_df, address_df, location_df):
    order_statuses = ['Delivered', 'Canceled', 'Failed', 'Returned']
    payment_methods = ['Cash', 'UPI', 'Wallet']
    
    data = []
    order_id = order_start_id
    
    # Add location information to address_df for easier joining
    address_with_location = pd.DataFrame()
    
    # For each customer, generate orders from restaurants in the same city as their address
    for customer_id in customer_df['CustomerID']:
        # Get all addresses for this customer
        customer_addresses = address_df[address_df['CustomerID'] == customer_id]
        
        if len(customer_addresses) == 0:
            continue
            
        # Generate 1-5 orders for this customer
        num_orders = random.randint(1, 5)
        
        for _ in range(num_orders):
            # Randomly select one of the customer's addresses
            address = customer_addresses.sample(1).iloc[0]
            address_id = address['AddressID']
            city = address['City']
            
            # Find restaurants in the same city
            city_location_ids = location_df[location_df['City'] == city]['LocationID'].tolist()
            city_restaurants = restaurant_df[restaurant_df['LocationID'].isin(city_location_ids)]
            
            # Skip if no restaurants found in this city
            if len(city_restaurants) == 0:
                continue
                
            # Select a random restaurant from the same city
            restaurant = city_restaurants.sample(1).iloc[0]
            restaurant_id = restaurant['RestaurantID']
            
            # Order date (last 90 days)
            order_date = fake.date_time_between(start_date='-90d', end_date='now')
            
            # Order amount (initially set to 0, will be updated later)
            total_amount = 0
            
            # Status
            # days_since_order = (datetime.now() - order_date).days
            hours_since_order = (datetime.now() - order_date).total_seconds() / 3600
            if hours_since_order > 2 :
                status = random.choices(
                    order_statuses, 
                    weights=[0.8, 0.1, 0.05, 0.05]
                )[0]
            else:
                status = random.choices(
                    ['Delivered', 'In Transit', 'Preparing'], 
                    weights=[0.6, 0.3, 0.1]
                )[0]
            
            # Payment method
            payment_method = random.choice(payment_methods)
            
            # Created and modified dates
            created_date = order_date
            modified_date = fake.date_time_between(start_date=created_date, end_date='now')
            
            data.append({
                'OrderID': order_id,
                'CustomerID': customer_id,
                'RestaurantID': restaurant_id,
                'OrderDate': order_date,
                'TotalAmount': total_amount,  # Will be updated after order items are generated
                'Status': status,
                'PaymentMethod': payment_method,
                'CreatedDate': created_date,
                'ModifiedDate': modified_date,
                'AddressID': address_id  # Temp field to link delivery
            })
            
            order_id += 1
        #     if order_id >= order_end_id:
        #         break
                
        # if order_id >= order_end_id:
        #     break
    
    result_df = pd.DataFrame(data)
    
    return result_df

def generate_order_items_data(order_df, menu_df):
    data = []
    order_item_id = 1
    
    # Get the mapping of restaurant to their menu items
    restaurant_menu_map = {}
    for _, menu_item in menu_df.iterrows():
        restaurant_id = menu_item['RestaurantID']
        menu_id = menu_item['MenuID']
        
        if restaurant_id not in restaurant_menu_map:
            restaurant_menu_map[restaurant_id] = []
            
        restaurant_menu_map[restaurant_id].append(menu_id)
    
    # For each order, generate 1-5 order items
    for _, order in order_df.iterrows():
        order_id = order['OrderID']
        restaurant_id = order['RestaurantID']
        
        # Get available menu items for this restaurant
        menu_ids = restaurant_menu_map.get(restaurant_id, [])
        
        if not menu_ids:
            continue
            
        # Generate 1-5 random order items
        num_items = random.randint(1, 5)
        # Select unique menu items
        selected_menu_ids = random.sample(menu_ids, min(num_items, len(menu_ids)))
        
        order_total = 0
        
        for menu_id in selected_menu_ids:
            # Get the menu item details
            menu_item = menu_df[menu_df['MenuID'] == menu_id].iloc[0]
            price = menu_item['Price']
            
            # Generate random quantity
            quantity = random.randint(1, 3)
            
            # Calculate subtotal
            subtotal = price * quantity
            order_total += subtotal
            
            # Dates
            created_date = order['CreatedDate']
            modified_date = order['ModifiedDate']
            
            data.append({
                'OrderItemID': order_item_id,
                'OrderID': order_id,
                'MenuID': menu_id,
                'Quantity': quantity,
                'Price': price,
                'Subtotal': subtotal,
                'CreatedDate': created_date,
                'ModifiedDate': modified_date
            })
            
            order_item_id += 1

        order_df.loc[order_df['OrderID'] == order_id, 'TotalAmount'] = order_total

    # Create the DataFrame
    order_items_df = pd.DataFrame(data)
    
    # Update the total amount in the orders DataFrame
    # order_totals = order_items_df.groupby('OrderID')['Subtotal'].sum().reset_index()

    return order_items_df


def generate_delivery_data(order_df, delivery_agent_df, delivery_start_id,restaurant_df):
    delivery_statuses = ['Delivered', 'In Transit', 'Assigned', 'Failed']
    
    data = []
    delivery_id = delivery_start_id
    
    # For each order, generate a delivery record
    for _, order in order_df.iterrows():
        order_id = order['OrderID']
        address_id = order['AddressID']
        
        # Only generate delivery for non-canceled orders
        if order['Status'] not in ['Canceled']:
            # Find delivery agents in the same city as the restaurant
            restaurant_id = order['RestaurantID']
            restaurant_location_id = restaurant_df[restaurant_df['RestaurantID'] == restaurant_id]['LocationID'].values[0]            
            available_agents = delivery_agent_df[delivery_agent_df['LocationID'] == restaurant_location_id]

            # Get delivery agents (we'll assume agents can deliver to any location)
            if len(available_agents) == 0:
                continue
                
            # Select a random delivery agent
            agent = available_agents.sample(1).iloc[0]
            agent_id = agent['DeliveryAgentID']
            
            # Set status based on order status
            if order['Status'] == 'Delivered':
                delivery_status = 'Delivered'
            elif order['Status'] == 'Failed':
                delivery_status = 'Failed'
            elif order['Status'] == 'Returned':
                delivery_status = 'Returned'
            else:
                delivery_status = random.choice(['In Transit', 'Assigned'])
            
            # Estimated time (10-60 minutes)
            estimated_time = f"{random.randint(10, 60)} minutes"
            
            # Delivery date based on order date
            if delivery_status == 'Delivered':
                # Add 30-90 minutes to order date
                minutes_to_add = random.randint(30, 90)
                delivery_date = order['OrderDate'] + timedelta(minutes=minutes_to_add)
            else:
                delivery_date = None
            
            # Dates
            created_date = order['CreatedDate']
            modified_date = order['ModifiedDate']
            
            data.append({
                'DeliveryID': delivery_id,
                'OrderID': order_id,
                'DeliveryAgentID': agent_id,
                'DeliveryStatus': delivery_status,
                'EstimatedTime': estimated_time,
                'AddressID': address_id,
                'DeliveryDate': delivery_date,
                'CreatedDate': created_date,
                'ModifiedDate': modified_date
            })
            
            delivery_id += 1
    
    return pd.DataFrame(data)


# def update_order_totals(order_df, order_totals):
#     # Create a dictionary for faster lookups
#     total_dict = dict(zip(order_totals['OrderID'], order_totals['Subtotal']))
    
#     # Update the orders DataFrame
#     for i, row in order_df.iterrows():
#         order_id = row['OrderID']
#         if order_id in total_dict:
#             order_df.at[i, 'TotalAmount'] = total_dict[order_id]
    
#     return order_df


# Main execution section
# if __name__ == "__main__":
# Generate location data
# print("Generating location data...")

# location_df = generate_location_data(LOCATION_START_ID, LOCATION_END_ID)
# print(location_df.to_string())
# location_df.to_csv('data/location.csv', index=False)


## Reading all files already generated
location_df = pd.read_csv('data/location.csv')
restaurant_df = pd.read_csv('data/restaurant.csv')
menu_df = pd.read_csv('data/menu.csv')
customer_df = pd.read_csv('data/customer.csv')
address_df = pd.read_csv('data/customer_address.csv')
login_audit_df = pd.read_csv('data/login_audit.csv')
delivery_agent_df = pd.read_csv('data/delivery_agent.csv')


# # Generate restaurant data
# restaurant_df = generate_restaurant_data(RESTAURANT_START_ID, RESTAURANT_END_ID, location_df)
# print(restaurant_df.to_string())

# # Generate menu data
# menu_df = generate_menu_data(MENU_START_ID, MENU_END_ID, restaurant_df)
# print(menu_df.to_string())

# # Generate customer data
customer_df = generate_customer_data(CUSTOMER_START_ID, CUSTOMER_END_ID)
print(customer_df.to_string())

# # Generate customer address data
# address_df = generate_customer_address_data(CUSTOMER_ADDRESS_START_ID, CUSTOMER_ADDRESS_END_ID, customer_df, location_df)
# print(address_df.to_string())

# # Generate login audit data
# login_audit_df = generate_login_audit_data(CUSTOMER_LOGIN_AUDIT_START_ID, CUSTOMER_LOGIN_AUDIT_END_ID, customer_df)
# print(login_audit_df.to_string())

# # Generate delivery agent data
# delivery_agent_df = generate_delivery_agent_data(DELIVERY_AGENT_START_ID, DELIVERY_AGENT_END_ID, location_df)
# print(delivery_agent_df.to_string())

# # Generate orders data
order_df = generate_orders_data(ORDER_START_ID, ORDER_END_ID, customer_df, restaurant_df, address_df, location_df)
# print(order_df.to_string())

# # Generate order items data
order_items_df = generate_order_items_data(order_df, menu_df)
# print(order_items_df.to_string())
# print(order_df.to_string())

# # Update order totals
# order_df = update_order_totals(order_df, order_totals)

# # Generate delivery data
delivery_df = generate_delivery_data(order_df, delivery_agent_df, DELIVERY_START_ID,restaurant_df)
# print(delivery_df.to_string())

    # Remove temporary columns
if 'AddressID' in order_df.columns:
    order_df = order_df.drop(columns=['AddressID'])

# if 'LocationID' in address_df.columns:
#     address_df =  address_df.drop(columns=['LocationID'])

    # Save all DataFrames to CSV files
    # print("Saving data to CSV files...")
    # location_df.to_csv('data/location.csv', index=False)
    

# location_df.to_csv('data/location.csv',index=False)
# restaurant_df.to_csv('data/restaurant.csv', index=False)
# menu_df.to_csv('data/menu.csv', index=False)
# customer_df.to_csv('data/customer.csv', index=False)
# address_df.to_csv('data/customer_address.csv', index=False)
# login_audit_df.to_csv('data/login_audit.csv', index=False)
# delivery_agent_df.to_csv('data/delivery_agent.csv', index=False)


# When Generaate data make sure file name is diffrent 
# order_df.to_csv('data1/orders.csv', index=False)
# order_items_df.to_csv('data1/order_items.csv', index=False)
# delivery_df.to_csv('data1/delivery.csv', index=False)
    