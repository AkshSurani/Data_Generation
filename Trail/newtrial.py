import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta, date
import json
import uuid
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Initialize Faker
fake = Faker('en_IN')  # Using Indian locale since example data appears to be from India

# Create output directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Define number of records to generate
num_records = 100

## LOCATIONS
NUM_LOCATIONS = 10  # Number of locations
LOCATION_START_ID = 1
LOCATION_END_ID = LOCATION_START_ID + NUM_LOCATIONS

## CUSTOMERS
NUM_CUSTOMERS = 100  # Number of customers
CUSTOMER_START_ID = 1
CUSTOMER_END_ID = CUSTOMER_START_ID + NUM_CUSTOMERS

## RESTAURANTS
NUM_RESTAURANTS = 20  # Number of restaurants
RESTAURANT_START_ID = 1
RESTAURANT_END_ID = RESTAURANT_START_ID + NUM_RESTAURANTS

## DELIVERY AGENTS
NUM_DELIVERY_AGENTS = 30  # Number of delivery agents
DELIVERY_AGENTS_START_ID = 1
DELIVERY_AGENTS_END_ID= DELIVERY_AGENTS_START_ID + NUM_DELIVERY_AGENTS

## ORDERS
NUM_ORDERS = 200  # Number of orders
ORDER_START_ID = 1
ORDER_END_ID = ORDER_START_ID + NUM_ORDERS

## CURRENT DATE FOR FILE SAVE 
CURRENT_DATE = datetime.now()


# =====================
# 1. Generate Location data
# =====================
def generate_location_data(location_start_id,location_end_id):
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
        ('Indore', 'Madhya Pradesh')
    ]
    
    data = []
    for i in range(location_start_id, location_end_id + 1):
        city, state = random.choice(cities_states)
        zipcode = f"{random.randint(110000, 999999)}"
        active_flag = random.choice(['Yes', 'No'] )
        created_date = fake.date_time_between(start_date='-3y', end_date='now')
        modified_date = fake.date_time_between(start_date=created_date, end_date='now') if random.random() > 0.3 else None
        
        data.append({
            'LocationID': i,
            'City': city,
            'State': state,
            'ZipCode': zipcode,
            'ActiveFlag': active_flag,
            'CreatedDate': created_date,
            'ModifiedDate': modified_date
        })
    
    return pd.DataFrame(data)

# =====================
# 2. Generate Restaurant data
# =====================
def generate_restaurant_data(num_records, location_df):
    # Cuisine types
    cuisine_types = [
        "North Indian", "South Indian", "Chinese", "Italian", "Continental", 
        "Mediterranean", "Mexican", "Thai", "Japanese", "Lebanese", 
        "Mughlai", "Street Food", "Desserts", "Beverages", "Fast Food",
        "Cafe", "Bakery", "Ice Cream", "Pizza", "Burger"
    ]
    
    # Restaurant names (first parts and second parts to combine)
    first_parts = ["Royal", "Spice", "Taste", "Flavors", "Urban", "Green", "Blue", "Red", 
                  "Golden", "Silver", "Diamond", "Emerald", "Crystal", "Pearl", "Ruby"]
    second_parts = ["Kitchen", "Bistro", "Restaurant", "Cafe", "Diner", "Eatery", "Grill", 
                   "Bites", "Table", "Garden", "House", "Palace", "Corner", "Junction", "Hub"]
    
    data = []
    for i in range(1, num_records + 1):
        # Generate restaurant name
        name = f"{random.choice(first_parts)} {random.choice(second_parts)}"
        
        # Generate cuisine types (1-3 random cuisine types)
        num_cuisines = random.randint(1, 3)
        restaurant_cuisines = random.sample(cuisine_types, num_cuisines)
        cuisine_type = ", ".join(restaurant_cuisines)
        
        # Other fields
        pricing_for_2 = random.randint(500, 5000)
        phone = f"9{random.randint(100000000, 999999999)}"
        
        # Opening and closing hours
        opening_hour = random.randint(7, 12)
        closing_hour = random.randint(17, 23)
        operating_hours = f"{opening_hour}:00 AM - {closing_hour}:00 PM"
        
        # Location details
        location_id = random.choice(location_df['LocationID'])
        active_flag = random.choice(['Yes', 'No'])
        open_status = 'Open' if active_flag == 'Yes' else 'Closed'
        
        # Address and locality
        locality = f"{fake.city_suffix()}, {fake.city()}"
        restaurant_address = fake.address().replace('\n', ', ')
        
        # Coordinates (latitude and longitude for India)
        latitude = random.uniform(8.0, 37.0)  # India's approximate latitude range
        longitude = random.uniform(68.0, 97.0)  # India's approximate longitude range
        
        # Dates
        created_date = fake.date_time_between(start_date='-3y', end_date='-1y')
        modified_date = fake.date_time_between(start_date=created_date, end_date='now')
        
        data.append({
            'RestaurantID': i,
            # 'Name': name,
            # 'CuisineType': cuisine_type,
            # 'Pricing_for_2': pricing_for_2,
            # 'Restaurant_Phone': phone,
            # 'OperatingHours': operating_hours,
            # 'LocationID': location_id,
            # 'ActiveFlag': active_flag,
            # 'OpenStatus': open_status,
            'Locality': locality,
            'Restaurant_Address': restaurant_address,
            # 'Latitude': latitude,
            # 'Longitude': longitude,
            # 'CreatedDate': created_date,
            # 'ModifiedDate': modified_date
        })
    
    return pd.DataFrame(data)

# =====================
# 3. Generate Menu data
# =====================
def generate_menu_data(num_records, restaurant_df):
    # Dictionary of meal categories and items
    menu_items = {
        'Appetizer': [
            'Spring Rolls', 'Garlic Bread', 'Bruschetta', 'Paneer Tikka', 'Chicken Wings',
            'Hummus', 'Nachos', 'Samosas', 'Manchurian', 'Onion Rings'
        ],
        'Main Course': [
            'Butter Chicken', 'Paneer Makhani', 'Pasta Arrabiata', 'Pizza Margherita',
            'Biryani', 'Fish Curry', 'Pad Thai', 'Burger', 'Noodles', 'Fried Rice'
        ],
        'Dessert': [
            'Gulab Jamun', 'Chocolate Cake', 'Ice Cream', 'Tiramisu', 'Cheesecake',
            'Kulfi', 'Brownie', 'Mousse', 'Pastry', 'Kheer'
        ],
        'Beverage': [
            'Coffee', 'Tea', 'Lemonade', 'Smoothie', 'Milkshake',
            'Soda', 'Juice', 'Cocktail', 'Mocktail', 'Water'
        ]
    }
    
    # Item types
    item_types = ['Veg', 'Non-Veg', 'Vegan']
    
    data = []
    menu_id = 1
    
    # Generate multiple menu items for each restaurant
    for restaurant_id in restaurant_df['RestaurantID']:
        # Number of menu items for this restaurant (5-15)
        num_items = random.randint(5, 15)
        
        # Restaurant's creation date for reference
        restaurant_created = restaurant_df.loc[restaurant_df['RestaurantID'] == restaurant_id, 'CreatedDate'].iloc[0]
        
        for _ in range(num_items):
            # Select random category and item
            category = random.choice(list(menu_items.keys()))
            item_name = random.choice(menu_items[category])
            
            # Generate description
            description = fake.text(max_nb_chars=100)
            
            # Price based on category
            if category == 'Appetizer':
                price = random.randint(100, 400)
            elif category == 'Main Course':
                price = random.randint(300, 800)
            elif category == 'Dessert':
                price = random.randint(150, 350)
            else:  # Beverage
                price = random.randint(50, 250)
            
            # Availability and item type
            availability = random.choice([True, True, True, False])  # More likely to be available
            item_type = random.choice(item_types)
            
            # Dates
            created_date = fake.date_time_between(start_date=restaurant_created, end_date=restaurant_created + timedelta(days=30))
            modified_date = fake.date_time_between(start_date=created_date, end_date='now') if random.random() > 0.3 else created_date
            
            data.append({
                'MenuID': menu_id,
                'RestaurantID': restaurant_id,
                'ItemName': item_name,
                'Description': description,
                'Price': price,
                'Category': category,
                'Availability': availability,
                'ItemType': item_type,
                'CreatedDate': created_date,
                'ModifiedDate': modified_date
            })
            
            menu_id += 1
            
            # Stop if we've reached the desired number of total menu items
            if menu_id > num_records:
                break
                
        if menu_id > num_records:
            break
    
    return pd.DataFrame(data)

# =====================
# 4. Generate Customer data
# =====================
def generate_customer_data(num_records):
    login_methods = ['GMail_Account', 'Facebook_Account', 'Apple_ID', 'Phone', 'Other_EMail']
    genders = ['Male', 'Female', 'Other', 'Corporate', 'Prefer not to say']
    
    food_preferences = ['Veg', 'Non-Veg', 'Vegan', 'Eggetarian']
    cuisine_types = ['North Indian', 'South Indian', 'Chinese', 'Italian', 'Continental', 
                      'Mediterranean', 'Mexican', 'Thai', 'Japanese', 'Lebanese']
    
    data = []
    for i in range(1, num_records + 1):
        # Basic info
        name = fake.name()
        mobile = f"{random.randint(7000000000, 9999999999)}"
        email_domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])
        email = f"{name.lower().replace(' ', '')}{random.randint(1, 999)}@{email_domain}"
        login_using = random.choice(login_methods)
        gender = random.choice(genders)
        
        # Generate random birth date (18-60 years old)
        dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
        
        # Generate anniversary date (0-30 years after birth date)
        years_after_dob = random.randint(21, 40)  # Most people marry after 21
        anniversary = date(dob.year + years_after_dob, random.randint(1, 12), random.randint(1, 28))
        
        # Generate food preferences
        food_pref = random.choice(food_preferences)
        num_cuisines = random.randint(1, 3)
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
            'Name': name,
            'Mobile': mobile,
            'Email': email,
            'LoginByUsing': login_using,
            'Gender': gender,
            'DOB': dob,
            'Anniversary': anniversary,
            'Preferences': json.dumps(preferences),
            'CreatedDate': created_date,
            'ModifiedDate': modified_date
        })
    
    return pd.DataFrame(data)

# =====================
# 5. Generate Customer Address Book data
# =====================
def generate_customer_address_data(num_records, customer_df):
    address_types = ['Home', 'Work', 'Other']
    
    data = []
    address_id = 1
    
    # Generate 1-3 addresses per customer
    for customer_id in customer_df['CustomerID']:
        # Number of addresses for this customer
        num_addresses = random.randint(1, 3)
        
        for _ in range(num_addresses):
            flat_no = str(random.randint(1, 100))
            house_no = str(random.randint(1, 100))
            floor = str(random.randint(1, 10))
            building = fake.company() + " " + random.choice(['Apartments', 'Residency', 'Heights', 'Towers', 'Complex'])
            landmark = "Near " + fake.company()
            
            # Locality, city, state
            locality = random.choice([
                'Saket', 'Connaught Place', 'Dwarka', 'Vasant Kunj', 'South Extension',
                'Rohini', 'Karol Bagh', 'Pitampura', 'Janakpuri', 'Lajpat Nagar',
                'Malviya Nagar', 'Greater Kailash', 'Hauz Khas', 'Mayur Vihar', 'Rajouri Garden'
            ])
            
            city = "New Delhi"
            state = "Delhi"
            pincode = random.randint(110001, 110096)
            
            # Coordinates
            latitude = random.uniform(-90, 90)
            longitude = random.uniform(-180, 180)
            coordinates = f"{latitude},{longitude}"
            
            # Primary flag (only one primary address per customer)
            primary_flag = "Yes" if _ == 0 else "No"
            address_type = random.choice(address_types)
            
            # Dates
            created_date = fake.date_time_between(start_date='-3y', end_date='-6m')
            modified_date = fake.date_time_between(start_date=created_date, end_date='now')
            
            data.append({
                'AddressID': address_id,
                'CustomerID': customer_id,
                'FlatNo': flat_no,
                'HouseNo': house_no,
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
                'ModifiedDate': modified_date
            })
            
            address_id += 1
            
            # Stop if we've reached the desired number
            if address_id > num_records:
                break
                
        if address_id > num_records:
            break
    
    return pd.DataFrame(data).head(num_records)

# =====================
# 6. Generate Login Audit data
# =====================
def generate_login_audit_data(num_records, customer_df):
    login_types = ['App', 'Web', 'Desktop']
    device_interfaces = ['Android', 'iOS', 'PWA']
    mobile_devices = ['iPhone', 'Samsung Galaxy', 'OnePlus', 'Xiaomi', 'Oppo', 'Vivo', 'Realme']
    web_interfaces = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
    
    data = []
    for i in range(1, num_records + 1):
        # Random customer
        customer_id = random.choice(customer_df['CustomerID'])
        
        # Login details
        login_type = random.choice(login_types)
        
        # Device details depend on login type
        if login_type == 'App':
            device_interface = random.choice(device_interfaces)
            mobile_device_name = random.choice(mobile_devices) if device_interface != 'PWA' else 'PWA'
            web_interface = None
        else:  # Web or Desktop
            device_interface = None
            mobile_device_name = None
            web_interface = random.choice(web_interfaces)
        
        # Login timestamp (last 30 days)
        last_login = fake.date_time_between(start_date='-30d', end_date='now')
        
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

# =====================
# 7. Generate Orders data
# =====================
def generate_orders_data(num_records, customer_df, restaurant_df):
    order_statuses = ['Placed', 'Preparing', 'Ready', 'Out for Delivery', 'Delivered', 'Cancelled']
    payment_methods = ['Card', 'UPI', 'COD', 'Wallet', 'NetBanking']
    
    data = []
    for i in range(1, num_records + 1):
        # Random customer and restaurant
        customer_id = random.choice(customer_df['CustomerID'])
        restaurant_id = random.choice(restaurant_df['RestaurantID'])
        
        # Order date (last 90 days)
        order_date = fake.date_time_between(start_date='-90d', end_date='now')
        
        # Order amount (based on restaurant's pricing_for_2)
        restaurant_price = restaurant_df.loc[restaurant_df['RestaurantID'] == restaurant_id, 'Pricing_for_2'].iloc[0]
        # Order for 1-4 people
        people_factor = random.uniform(0.5, 2.0)
        total_amount = round(restaurant_price * people_factor, 2)
        
        # Status (more likely to be Delivered for older orders)
        days_since_order = (datetime.now() - order_date).days
        if days_since_order > 2:
            status = random.choices(
                order_statuses, 
                weights=[0.05, 0.05, 0.05, 0.05, 0.7, 0.1]
            )[0]
        else:
            status = random.choices(
                order_statuses, 
                weights=[0.2, 0.2, 0.2, 0.2, 0.1, 0.1]
            )[0]
        
        # Payment method
        payment_method = random.choice(payment_methods)
        
        # Dates
        created_date = order_date
        modified_date = fake.date_time_between(start_date=created_date, end_date=created_date + timedelta(hours=2))
        
        data.append({
            'OrderID': i,
            'CustomerID': customer_id,
            'RestaurantID': restaurant_id,
            'OrderDate': order_date,
            'TotalAmount': total_amount,
            'Status': status,
            'PaymentMethod': payment_method,
            'CreatedDate': created_date,
            'ModifiedDate': modified_date
        })
    
    return pd.DataFrame(data)

# =====================
# 8. Generate Order Items data
# =====================
def generate_order_item_data(num_records, order_df, menu_df):
    data = []
    order_item_id = 1
    
    # Generate 1-5 items per order
    for order_id in order_df['OrderID']:
        # Restaurant ID for this order
        restaurant_id = order_df.loc[order_df['OrderID'] == order_id, 'RestaurantID'].iloc[0]
        
        # Get menu items for this restaurant
        restaurant_menu = menu_df[menu_df['RestaurantID'] == restaurant_id]
        
        if len(restaurant_menu) > 0:
            # Number of items in this order
            num_items = random.randint(1, min(5, len(restaurant_menu)))
            
            # Select random menu items
            selected_items = restaurant_menu.sample(num_items)
            
            for _, item in selected_items.iterrows():
                menu_id = item['MenuID']
                price = item['Price']
                
                # Quantity
                quantity = random.randint(1, 3)
                
                # Subtotal
                subtotal = price * quantity
                
                # Dates (same as order creation date)
                order_created = order_df.loc[order_df['OrderID'] == order_id, 'CreatedDate'].iloc[0]
                
                data.append({
                    'OrderItemID': order_item_id,
                    'OrderID': order_id,
                    'MenuID': menu_id,
                    'Quantity': quantity,
                    'Price': price,
                    'Subtotal': subtotal,
                    'CreatedDate': order_created,
                    'ModifiedDate': order_created
                })
                
                order_item_id += 1
                
                # Stop if we've reached the desired number
                if order_item_id > num_records:
                    break
                    
            if order_item_id > num_records:
                break
    
    return pd.DataFrame(data).head(num_records)

# =====================
# 9. Generate Delivery Agent data
# =====================
def generate_delivery_agent_data(num_records, location_df):
    vehicle_types = ['Bike', 'Bicycle', 'Scooter', 'Car']
    agent_statuses = ['Active', 'Inactive', 'On Leave']
    genders = ['Male', 'Female', 'Other', 'Prefer not to say']
    
    data = []
    for i in range(1, num_records + 1):
        # Basic info
        name = fake.name()
        phone = f"{random.randint(7000000000, 9999999999)}"
        vehicle_type = random.choice(vehicle_types)
        location_id = random.choice(location_df['LocationID'])
        status = random.choice(agent_statuses)
        gender = random.choice(genders)
        
        # Rating (1.0 to 5.0)
        rating = round(random.uniform(3.0, 5.0), 1)
        
        # Dates
        created_date = fake.date_time_between(start_date='-2y', end_date='-3m')
        modified_date = fake.date_time_between(start_date=created_date, end_date='now')
        
        data.append({
            'DeliveryAgentID': i,
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
    
    return pd.DataFrame(data)

# =====================
# 10. Generate Delivery data
# =====================
def generate_delivery_data(num_records, order_df, delivery_agent_df, address_df):
    delivery_statuses = ['Assigned', 'Picked Up', 'In Transit', 'Delivered', 'Cancelled']
    
    data = []
    for i in range(1, num_records + 1):
        # Only create deliveries for orders that are not cancelled
        valid_orders = order_df[order_df['Status'] != 'Cancelled']
        
        if len(valid_orders) == 0:
            continue
            
        # Random order
        order_row = valid_orders.sample(1).iloc[0]
        order_id = order_row['OrderID']
        
        # Customer from order
        customer_id = order_row['CustomerID']
        
        # Get customer's addresses
        customer_addresses = address_df[address_df['CustomerID'] == customer_id]
        
        if len(customer_addresses) == 0:
            continue
            
        # Use random address (prefer primary)
        primary_addresses = customer_addresses[customer_addresses['PrimaryFlag'] == 'Yes']
        if len(primary_addresses) > 0:
            address_id = primary_addresses.iloc[0]['AddressID']
        else:
            address_id = customer_addresses.sample(1).iloc[0]['AddressID']
        
        # Random delivery agent
        active_agents = delivery_agent_df[delivery_agent_df['Status'] == 'Active']
        if len(active_agents) > 0:
            delivery_agent_id = active_agents.sample(1).iloc[0]['DeliveryAgentID']
        else:
            delivery_agent_id = delivery_agent_df.sample(1).iloc[0]['DeliveryAgentID']
        
        # Status based on order status
        order_status = order_row['Status']
        if order_status == 'Delivered':
            delivery_status = 'Delivered'
        elif order_status == 'Cancelled':
            delivery_status = 'Cancelled'
        elif order_status == 'Out for Delivery':
            delivery_status = 'In Transit'
        elif order_status == 'Ready':
            delivery_status = 'Picked Up'
        else:
            delivery_status = 'Assigned'
        
        # Estimated time (20-60 minutes)
        estimated_minutes = random.randint(20, 60)
        estimated_time = f"00:{estimated_minutes}:00"
        
        # Delivery date (based on order date)
        order_date = order_row['OrderDate']
        delivery_date = order_date + timedelta(minutes=random.randint(30, 90))
        
        # Dates
        created_date = order_date
        modified_date = delivery_date if delivery_status == 'Delivered' else fake.date_time_between(start_date=created_date, end_date='now')
        
        data.append({
            'DeliveryID': i,
            'OrderID': order_id,
            'DeliveryAgentID': delivery_agent_id,
            'DeliveryStatus': delivery_status,
            'EstimatedTime': estimated_time,
            'AddressID': address_id,
            'DeliveryDate': delivery_date,
            'CreatedDate': created_date,
            'ModifiedDate': modified_date,
            'DeliveryAddress': address_id  # Same as AddressID as per schema
        })
    
    return pd.DataFrame(data)

# Generate all data
print("Generating location data...")
location_df = generate_location_data(LOCATION_START_ID,LOCATION_END_ID)

print("Generating restaurant data...")
restaurant_df = generate_restaurant_data(num_records, location_df)

print("Generating menu data...")
menu_df = generate_menu_data(num_records, restaurant_df)

print("Generating customer data...")
customer_df = generate_customer_data(num_records)

print("Generating customer address data...")
address_df = generate_customer_address_data(num_records, customer_df)

print("Generating login audit data...")
login_audit_df = generate_login_audit_data(num_records, customer_df)

print("Generating orders data...")
orders_df = generate_orders_data(num_records, customer_df, restaurant_df)

print("Generating order item data...")
order_item_df = generate_order_item_data(num_records, orders_df, menu_df)

print("Generating delivery agent data...")
delivery_agent_df = generate_delivery_agent_data(num_records, location_df)

print("Generating delivery data...")
delivery_df = generate_delivery_data(num_records, orders_df, delivery_agent_df, address_df)

# Save all dataframes to CSV
print("Saving data to CSV files...")
print(restaurant_df)
location_df.to_csv('data/location.csv', index=False)
restaurant_df.to_csv('data/restaurant.csv', index=False)
menu_df.to_csv('data/menu.csv', index=False)
customer_df.to_csv('data/customer.csv', index=False)
address_df.to_csv('data/customer_address.csv', index=False)
login_audit_df.to_csv('data/login_audit.csv', index=False)
orders_df.to_csv('data/orders.csv', index=False)
order_item_df.to_csv('data/order_item.csv', index=False)
delivery_agent_df.to_csv('data/delivery_agent.csv', index=False)
delivery_df.to_csv('data/delivery.csv', index=False)

print("Data generation complete. Files saved to the 'data' directory.")


''' 
1) location.csv-> Done!!!
    - Active flag ma 90% yes hovi joia

2) restaurant.csv->
    -as per the location locality and restaurantAdd avvu joia ---> ama atyare restaurant add kaik alag j ave chhe
     locality ma agal ville ave chhe e na avvu joia
    -active flag and openstatus mostly yes and open aavu joia 

3) customer.csv->
    -Gender ma 95% male female avvu joia 
    -anniversary ma 2025 up ekey date na hovi joia je aama chhe etle evi kaik condition muk k 2000 up jenu born hoy ane j anniversary ave baki nai 
     if jo 2004 born year hoy to ena mate anniversary vala ma balnk avvu joia

4) customer_address.csv->
    -bdha customerAdd only delhi na j chhe so change that 

5) login_audit.csv->
    -login type only web or mobile
    -device interface web-web, mobile-android or ios
    -mobiledevice and webinterface as per the chhose login type if it's mobile so name the mobiledevicename and blank the web interface.

6) menu.csv-> done both changes 
    -change the description for particular itemname
    -increase the avialability 

7) orders.csv->
    -no changes.

8) orderitem.csv->
    change the modified date.

9) delivery_agent.csv -> 
    vehical type should only contain bike and scooter, remove car & bicycle
    gender ma male ni probability high rakhvani

10) delivery.csv->
    change the deliverydate and modified date.

'''





# Change code  

# import pandas as pd
# import numpy as np
# from faker import Faker
# import random
# from datetime import datetime, timedelta, date
# import json
# import uuid
# import os

# # Set random seed for reproducibility
# np.random.seed(42)
# random.seed(42)

# # Initialize Faker
# fake = Faker('en_IN')  # Using Indian locale since example data appears to be from India

# # Create output directory if it doesn't exist
# if not os.path.exists('data'):
#     os.makedirs('data')

# # Define number of records to generate
# num_records = 100

# ## LOCATIONS
# NUM_LOCATIONS = 5  # Number of locations
# LOCATION_START_ID = 1
# LOCATION_END_ID = LOCATION_START_ID + NUM_LOCATIONS

# ## RESTAURANTS
# NUM_RESTAURANTS = 10  # Number of restaurants
# RESTAURANT_START_ID = 1
# RESTAURANT_END_ID = RESTAURANT_START_ID + NUM_RESTAURANTS

# ## MENU
# NUM_MENU = 100  # Number of orders
# MENU_START_ID = 1
# MENU_END_ID = MENU_START_ID + NUM_MENU

# ## CUSTOMERS
# NUM_CUSTOMERS = 10  # Number of customers
# CUSTOMER_START_ID = 1
# CUSTOMER_END_ID = CUSTOMER_START_ID + NUM_CUSTOMERS

# ## CUSTOMER ADDRESS
# NUM_CUSTOMER_ADDRESS = 20
# CUSTOMER_ADDRESS_START_ID = 1
# CUSTOMER_ADDRESS_END_ID = CUSTOMER_START_ID + NUM_CUSTOMER_ADDRESS

# ## CUSTOMER LOGIN AUDIT
# NUM_CUSTOMER_LOGIN_AUDIT = 50
# CUSTOMER_LOGIN_AUDIT_START_ID = 1
# CUSTOMER_LOGIN_AUDIT_END_ID = CUSTOMER_LOGIN_AUDIT_START_ID + NUM_CUSTOMER_LOGIN_AUDIT

# ## ORDERS
# NUM_ORDERS = 200  # Number of orders
# ORDER_START_ID = 1
# ORDER_END_ID = ORDER_START_ID + NUM_ORDERS

# ## DELIVERY AGENTS
# NUM_DELIVERY_AGENT = 50  # Number of delivery agents
# DELIVERY_AGENT_START_ID = 1
# DELIVERY_AGENT_END_ID= DELIVERY_AGENT_START_ID + NUM_DELIVERY_AGENT

# ## CURRENT DATE FOR FILE SAVE 
# CURRENT_DATE = datetime.now()


# # =====================
# # 1. Generate Location data
# # =====================
# def generate_location_data(location_start_id,location_end_id):
#     # Indian cities and states
#     cities_states = [
#         ('Delhi', 'Delhi'),
#         ('Mumbai', 'Maharashtra'),
#         ('Bangalore', 'Karnataka'),
#         ('Hyderabad', 'Telangana'),
#         ('Chennai', 'Tamil Nadu'),
#         ('Kolkata', 'West Bengal'),
#         ('Pune', 'Maharashtra'),
#         ('Ahmedabad', 'Gujarat'),
#         ('Jaipur', 'Rajasthan'),
#         ('Lucknow', 'Uttar Pradesh'),
#         ('Chandigarh', 'Punjab'),
#         ('Bhopal', 'Madhya Pradesh'),
#         ('Guwahati', 'Assam'),
#         ('Kochi', 'Kerala'),
#         ('Indore', 'Madhya Pradesh')
#     ]
    
#     data = []
#     for i in range(location_start_id, location_end_id):
#         city, state = random.choice(cities_states)
#         zipcode = f"{random.randint(110000, 999999)}"
#         active_flag = np.random.choice(['Yes', 'No'], p =  [0.9,0.1])
#         created_date = fake.date_time_between(start_date='-3y', end_date='now')
#         modified_date = fake.date_time_between(start_date=created_date, end_date='now') if random.random() > 0.3 else None
        
#         data.append({
#             'LocationID': i,
#             'City': city,
#             'State': state,
#             'ZipCode': zipcode,
#             'ActiveFlag': active_flag,
#             'CreatedDate': created_date,
#             'ModifiedDate': modified_date
#         })
    
#     return pd.DataFrame(data)

# # =====================
# # 2. Generate Restaurant data
# # =====================
# def generate_restaurant_data(restaurant_start_id,restaurant_end_id, location_df):
#     # Cuisine types
#     cuisine_types = [
#         "North Indian", "South Indian", "Chinese", "Italian", "Continental", 
#         "Mediterranean", "Mexican", "Thai", "Japanese", "Lebanese", 
#         "Mughlai", "Street Food", "Desserts", "Beverages", "Fast Food",
#         "Cafe", "Bakery", "Ice Cream", "Pizza", "Burger"
#     ]
    
#     # Restaurant names (first parts and second parts to combine)
#     first_parts = ["Royal", "Spice", "Taste", "Flavors", "Urban", "Green", "Blue", "Red", 
#                   "Golden", "Silver", "Diamond", "Emerald", "Crystal", "Pearl", "Ruby"]
#     second_parts = ["Kitchen", "Bistro", "Restaurant", "Cafe", "Diner", "Eatery", "Grill", 
#                    "Bites", "Table", "Garden", "House", "Palace", "Corner", "Junction", "Hub"]
    
#     data = []
#     for i in range(restaurant_start_id, restaurant_end_id):
#         # Generate restaurant name
#         name = f"{random.choice(first_parts)} {random.choice(second_parts)}"
        
#         # Generate cuisine types (1-3 random cuisine types)
#         num_cuisines = random.randint(1, 3)
#         restaurant_cuisines = random.sample(cuisine_types, num_cuisines)
#         cuisine_type = ", ".join(restaurant_cuisines)
        
#         # Other fields
#         pricing_for_2 = random.randint(200, 2000)
#         phone = f"9{random.randint(100000000, 999999999)}"
        
#         # Opening and closing hours
#         opening_hour = random.randint(7, 12)
#         closing_hour = random.randint(17, 23)
#         operating_hours = f"{opening_hour}:00 AM - {closing_hour}:00 PM"
        
#         # Location details
#         location_id = random.choice(location_df['LocationID'])
#         active_flag = np.random.choice(['Yes', 'No'],p=[0.9,0.1])
#         open_status = 'Open' if active_flag == 'Yes' else 'Closed'

#         # Address and locality
#         locality = f"{fake.street_name()}"
#         city_name_for_address = location_df[location_df['LocationID'] == location_id]['City'].values[0] 
#         city_pincode_for_address = location_df[location_df['LocationID'] == location_id]['ZipCode'].values[0]
#         restaurant_address = f'{f" {random.choice(['Ground Floor,','First Floor,','Second Floor,','Third Floor,'])}" if np.random.choice([True, False], p = [0.6,0.4]) else ""} {locality}, {city_name_for_address} - {city_pincode_for_address}'
        
#         # Coordinates (latitude and longitude for India)
#         latitude = random.uniform(8.0, 37.0)  # India's approximate latitude range
#         longitude = random.uniform(68.0, 97.0)  # India's approximate longitude range
        
#         # Dates
#         created_date = fake.date_time_between(start_date='-3y', end_date='-1y')
#         modified_date = fake.date_time_between(start_date=created_date, end_date='now')
        
#         data.append({
#             'RestaurantID': i,
#             'Name': name,
#             'CuisineType': cuisine_type,
#             'Pricing_for_2': pricing_for_2,
#             'Restaurant_Phone': phone,
#             'OperatingHours': operating_hours,
#             'LocationID': location_id,
#             'ActiveFlag': active_flag,
#             'OpenStatus': open_status,
#             'Locality': locality,
#             'Restaurant_Address': restaurant_address,
#             'Latitude': latitude,
#             'Longitude': longitude,
#             'CreatedDate': created_date,
#             'ModifiedDate': modified_date
#         })
    
#     return pd.DataFrame(data)


# def generate_menu_data(menu_start_id,menu_end_id, restaurant_df):
#     categories = ["Appetizers", "Main Course", "Desserts", "Beverages", "Snacks"]
#     # item_types = {
#     #     "Appetizers": ["Veg", "Non-Veg"],
#     #     "Main Course": ["Veg", "Non-Veg"],
#     #     "Desserts": ["Veg"],
#     #     "Beverages": ["Veg"],
#     #     "Snacks": ["Veg"]
#     # }
#     item_names = {
#         "Appetizers": ["Samosa", "Paneer Tikka", "Chicken Tikka", "Aloo Tikki", "Fish Fry", "Spring Rolls", "Hara Bhara Kebab", "Seekh Kebab", "Chicken Wings", "Prawn Skewers"],
#         "Main Course": ["Butter Chicken", "Paneer Butter Masala", "Dal Makhani", "Chole Bhature", "Biryani", "Rogan Josh", "Palak Paneer", "Malai Kofta", "Mutton Curry", "Fish Curry"],
#         "Desserts": ["Gulab Jamun", "Rasgulla", "Kheer", "Jalebi", "Kulfi", "Ras Malai", "Gajar Halwa", "Mysore Pak", "Peda", "Sandesh"],
#         "Beverages": ["Masala Chai", "Lassi", "Nimbu Pani", "Cold Coffee", "Fruit Juice", "Coconut Water", "Aam Panna", "Buttermilk", "Thandai", "Falooda"],
#         "Snacks": ["Pav Bhaji", "Bhel Puri", "Pani Puri", "Vada Pav", "Pakora", "Dhokla", "Kachori", "Sev Puri", "Dabeli", "Aloo Chaat"]
#     }
#     descriptions = ["Delicious and authentic {}.", "A popular Indian dish.", "Traditional Indian {} with rich flavors.", "A must-try {} from India.", "Classic {} with a twist."]
    
#     data = []
#     for i in range(menu_start_id,menu_end_id):
#         category = random.choice(categories)
#         item_name = random.choice(item_names[category])

#         if (item_name in ["Chicken Tikka", "Fish Fry", "Seekh Kebab", "Chicken Wings", "Prawn Skewers", "Butter Chicken", "Biryani", "Rogan Josh", "Mutton Curry", "Fish Curry"]) :
#             item_type = "Non-Veg"

#         else:
#             item_type = "Veg"
        
#         restaurant_id = random.choice(restaurant_df['RestaurantID'])
#         description = random.choice(descriptions).format(item_name)
#         price = random.randint(50, 500)
#         created_date = fake.date_time_between(start_date='-3y', end_date='-1y')
#         modified_date = fake.date_time_between(start_date=created_date, end_date='now')

#         data.append({
#             "MenuID": i,
#             "RestaurantID": restaurant_id,
#             "ItemName": item_name,
#             "Description": description,
#             "Price": price,
#             "Category": category,
#             "Availability": True,
#             "ItemType": item_type,
#             "CreatedDate": created_date,
#             "ModifiedDate": modified_date
#         })

#     return pd.DataFrame(data)


# def generate_customer_data(customer_start_id,customer_end_id):
#     login_methods = ['GMail_Account', 'Apple_ID', 'Other_EMail']
#     genders = ['Male', 'Female', 'Other']
    
#     food_preferences = ['Veg', 'Non-Veg', 'Vegan', 'Eggetarian']
#     cuisine_types = ['North Indian', 'South Indian', 'Chinese', 'Italian', 'Continental', 
#                       'Mediterranean', 'Mexican', 'Thai', 'Japanese', 'Lebanese']
    
#     data = []
#     for i in range(customer_start_id, customer_end_id):
#         # Basic info
#         name = fake.name()
#         mobile = f"{random.randint(7000000000, 9999999999)}"
#         email_domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])
#         email = f"{name.lower().replace(' ', '')}{random.randint(1, 999)}@{email_domain}"
#         login_using = random.choice(login_methods)
#         gender = random.choice(genders)
        
#         # Generate random birth date (18-60 years old)
#         # dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
        
#         # Generate anniversary date (0-30 years after birth date)
#         years_after_dob = random.randint(21, 40)  # Most people marry after 21
#         # anniversary = date(dob.year + years_after_dob, random.randint(1, 12), random.randint(1, 28))
#         dob = fake.date_of_birth(minimum_age=15, maximum_age=75)
#         anniversary = dob + timedelta(days=random.randint(365 * 18, 365 * 30))

#         # Generate food preferences
#         food_pref = random.choice(food_preferences)
#         num_cuisines = random.randint(1, 3)
#         cuisine_pref = random.sample(cuisine_types, num_cuisines)
        
#         preferences = {
#             'FoodPreference': food_pref,
#             'CuisineTypes': cuisine_pref
#         }
        
#         # Dates
#         created_date = fake.date_time_between(start_date='-3y', end_date='-1m')
#         modified_date = fake.date_time_between(start_date=created_date, end_date='now')

#         anniversary = anniversary if anniversary < datetime.date(CURRENT_DATE) else None
#         anniversary = np.random.choice([anniversary,None],p = [0.7,0.3])
#         data.append({
#             'CustomerID': i,
#             'Name': name,
#             'Mobile': mobile,
#             'Email': email,
#             'LoginByUsing': login_using,
#             'Gender': gender,
#             'DOB': dob,
#             'Anniversary': anniversary,
#             'Preferences': json.dumps(preferences),
#             'CreatedDate': created_date,
#             'ModifiedDate': modified_date
#         })
    
#     return pd.DataFrame(data)


# def generate_customer_address_data(customer_address_start_id,customer_address_end_id, customer_df):
#     address_types = ['Home', 'Work', 'Other']
    
#     data = []
#     address_id = customer_address_start_id
#     cities_states = [
#         ('Delhi', 'Delhi'),
#         ('Mumbai', 'Maharashtra'),
#         ('Bangalore', 'Karnataka'),
#         ('Hyderabad', 'Telangana'),
#         ('Chennai', 'Tamil Nadu'),
#         ('Kolkata', 'West Bengal'),
#         ('Pune', 'Maharashtra'),
#         ('Ahmedabad', 'Gujarat'),
#         ('Jaipur', 'Rajasthan'),
#         ('Lucknow', 'Uttar Pradesh'),
#         ('Chandigarh', 'Punjab'),
#         ('Bhopal', 'Madhya Pradesh'),
#         ('Guwahati', 'Assam'),
#         ('Kochi', 'Kerala'),
#         ('Indore', 'Madhya Pradesh')
#     ]
#     # Generate 1-3 addresses per customer
#     for customer_id in customer_df['CustomerID']:
#         # Number of addresses for this customer
#         num_addresses = random.randint(1, 3)
        
#         for _ in range(num_addresses):
#             flat_no = str(random.randint(1, 100))
#             house_no = str(random.randint(1, 100))
#             floor = str(random.randint(1, 10))
#             building = fake.company() + " " + random.choice(['Apartments', 'Residency', 'Heights', 'Towers', 'Complex'])
#             landmark = "Near " + fake.company()
            
#             # Locality, city, state
#             locality = random.choice([
#                 'Saket', 'Connaught Place', 'Dwarka', 'Vasant Kunj', 'South Extension',
#                 'Rohini', 'Karol Bagh', 'Pitampura', 'Janakpuri', 'Lajpat Nagar',
#                 'Malviya Nagar', 'Greater Kailash', 'Hauz Khas', 'Mayur Vihar', 'Rajouri Garden'
#             ])
            

#             city, state = random.choice(cities_states)
#             pincode = random.randint(110001, 999999)
            
#             # Coordinates
#             latitude = random.uniform(8.0, 37.0)  # India's approximate latitude range
#             longitude = random.uniform(68.0, 97.0)  # India's approximate longitude range
#             coordinates = f"{latitude},{longitude}"
            
#             # Primary flag (only one primary address per customer)
#             primary_flag = "Yes" if _ == 0 else "No"
#             address_type = random.choice(address_types)
            
#             # Dates
#             customer_created_date = customer_df[customer_df['CustomerID'] == customer_id]['CreatedDate'].values[0]
#             # print(customer_created_date)
#             created_date = fake.date_time_between(start_date='-3y', end_date='-6m')
#             modified_date = fake.date_time_between(start_date=created_date, end_date='now')
            

#             data.append({
#                 # 'AddressID': address_id,
#                 # 'CustomerID': customer_id,
#                 # 'Flat/House No.': flat_no,
#                 # 'Floor': floor,
#                 # 'Building': building,
#                 # 'Landmark': landmark,
#                 # 'Locality': locality,
#                 'City': city,
#                 'State': state,
#                 'Pincode': pincode,
#                 'Coordinates': coordinates,
#                 'PrimaryFlag': primary_flag,
#                 'AddressType': address_type,
#                 'CreatedDate': created_date,
#                 'ModifiedDate': modified_date
#             })
            
#             address_id += 1
            
#             # Stop if we've reached the desired number
#             if address_id > customer_address_end_id:
#                 break
                
#         if address_id > customer_address_end_id:
#             break
    
#     return pd.DataFrame(data)


# def generate_login_audit_data(customer_login_audit_start_id,customer_login_audit_end_id, customer_df):
#     login_types = ['App', 'Web']
#     device_interfaces = ['Android', 'iOS']
#     mobile_devices = ['Samsung Galaxy', 'OnePlus', 'Xiaomi', 'Oppo', 'Vivo', 'Realme']
#     web_interfaces = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
    
#     data = []
#     for i in range(customer_login_audit_start_id,customer_login_audit_end_id):
#         # Random customer
#         customer_id = random.choice(customer_df['CustomerID'])
        
#         # Login details
#         login_type = np.random.choice(login_types,p=[0.9,0.1])
        
#         # Device details depend on login type
#         if login_type == 'App':
#             device_interface = np.random.choice(device_interfaces, p=[0.7, 0.3])
#             mobile_device_name= 'iPhone' if device_interface=='iOS' else random.choice(mobile_devices)
#             web_interface = None
#         else:  # Web or Desktop
#             device_interface = None
#             mobile_device_name = None
#             web_interface = random.choice(web_interfaces)
        
#         # Login timestamp (last 30 days)
#         last_login = fake.date_time_between(start_date='-3y', end_date='now')
        
#         data.append({
#             'LoginID': i,
#             'CustomerID': customer_id,
#             'LoginType': login_type,
#             'DeviceInterface': device_interface,
#             'MobileDeviceName': mobile_device_name,
#             'WebInterface': web_interface,
#             'LastLogin': last_login
#         })
    
#     return pd.DataFrame(data)

# # =====================
# # 7. Generate Orders data
# # =====================

# # =====================
# # 7. Generate Orders data
# # =====================
# def generate_orders_data(num_records, customer_df, restaurant_df):
#     order_statuses = ['Delivered', 'Canceled', 'Failed', 'Returned', 'Abandoned']
#     payment_methods = ['Cash', 'UPI', 'Wallet']
    
#     data = []
#     for i in range(1, num_records + 1):
#         # Random customer and restaurant
#         customer_id = random.choice(customer_df['CustomerID'])
#         restaurant_id = random.choice(restaurant_df['RestaurantID'])
        
#         # Order date (last 90 days)
#         order_date = fake.date_time_between(start_date='-90d', end_date='now')
        
#         # Order amount (initially set to 0, will be updated later)
#         total_amount = 0
        
#         # Status (more likely to be Delivered for older orders)
#         days_since_order = (datetime.now() - order_date).days
#         if days_since_order > 2:
#             status = random.choices(
#                 order_statuses, 
#                 weights=[0.7, 0.1, 0.05, 0.05, 0.1]
#             )[0]
#         else:
#             status = random.choices(
#                 order_statuses, 
#                 weights=[0.1, 0.1, 0.2, 0.2, 0.4]
#             )[0]
        
#         # Payment method
#         payment_method = random.choice(payment_methods)
        
#         # Dates
#         created_date = order_date
#         modified_date = fake.date_time_between(start_date=created_date, end_date=created_date + timedelta(hours=2))
        
#         data.append({
#             'OrderID': i,
#             'CustomerID': customer_id,
#             'RestaurantID': restaurant_id,
#             'OrderDate': order_date,
#             'TotalAmount': total_amount,
#             'Status': status,
#             'PaymentMethod': payment_method,
#             'CreatedDate': created_date,
#             'ModifiedDate': modified_date
#         })
    
#     return pd.DataFrame(data)

# # =====================
# # 8. Generate Order Items data
# # =====================
# def generate_order_item_data(order_df, menu_df):
#     data = []
#     order_item_id = 1
    
#     for order_id in order_df['OrderID']:
#         # Restaurant ID for this order
#         restaurant_id = order_df.loc[order_df['OrderID'] == order_id, 'RestaurantID'].iloc[0]
        
#         # Get menu items for this restaurant
        
#         restaurant_menu = menu_df[menu_df['RestaurantID'] == restaurant_id]
        
#         if len(restaurant_menu) > 0:
#             # Number of items in this order
#             num_items = random.randint(1, min(5, len(restaurant_menu)))
            
#             # Select random menu items
#             selected_items = restaurant_menu.sample(num_items)
#             # print(selected_items)
#             # print(num_items)
#             order_total = 0
#             for _, item in selected_items.iterrows():
#                 menu_id = item['MenuID']
#                 price = item['Price']
                
#                 # Quantity
#                 quantity = random.randint(1, 3)
                
#                 # Subtotal
#                 subtotal = price * quantity
#                 order_total += subtotal
                
#                 # Dates (same as order creation date)
#                 order_created = order_df.loc[order_df['OrderID'] == order_id, 'CreatedDate'].iloc[0]
                
#                 data.append({
#                     'OrderItemID': order_item_id,
#                     'OrderID': order_id,
#                     'MenuID': menu_id,
#                     'Quantity': quantity,
#                     'Price': price,
#                     'Subtotal': subtotal,
#                     'CreatedDate': order_created,
#                     'ModifiedDate': order_created
#                 })
                
#                 order_item_id += 1
            
#             # Update the total amount in the orders table
#             order_df.loc[order_df['OrderID'] == order_id, 'TotalAmount'] = order_total
    
#     return pd.DataFrame(data), order_df

# # Example usage:
# customer_df = pd.DataFrame({'CustomerID': [1, 2, 3, 4, 5]})
# restaurant_df = pd.DataFrame({'RestaurantID': [1, 2, 3, 4, 5], 'Pricing_for_2': [500, 1000, 1500, 2000, 2500]})
# menu_df = pd.DataFrame({'MenuID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'RestaurantID': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 'Price': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]})

# orders_df = generate_orders_data(10, customer_df, restaurant_df)
# order_items_df, updated_orders_df = generate_order_item_data(orders_df, menu_df)

# print(updated_orders_df)
# print(order_items_df)


# # =====================
# # 9. Generate Delivery Agent data
# # =====================
# def generate_delivery_agent_data(delivery_agents_start_id,delivery_agent_end_id, location_df):
#     vehicle_types = ['Bike', 'Scooter']
    
#     data = []
#     for i in range(delivery_agents_start_id, delivery_agent_end_id):
#         # Basic info
#         name = fake.name()
#         phone = f"{random.randint(7000000000, 9999999999)}"
#         vehicle_type = random.choice(vehicle_types)
#         location_id = random.choice(location_df['LocationID'])
#         status = np.random.choice(['Active', 'Inactive'], p = [0.9,0.1])
#         gender = np.random.choice(['Male', 'Female', 'Other'],p=[0.9,0.09,0.01])
        
#         if gender == 'Male':
#             name = fake.name_male()
#         elif gender == 'Female':
#             name = fake.name_female()
            


#         # Rating (1.0 to 5.0)
#         rating = round(random.uniform(3.0, 5.0), 1)
        
#         # Dates
#         created_date = fake.date_time_between(start_date='-2y', end_date='-3m')
#         modified_date = fake.date_time_between(start_date=created_date, end_date='now')
        
#         data.append({
#             'DeliveryAgentID': i,
#             'Name': name,
#             'Phone': phone,
#             'VehicleType': vehicle_type,
#             'LocationID': location_id,
#             'Status': status,
#             'Gender': gender,
#             'Rating': rating,
#             'CreatedDate': created_date,
#             'ModifiedDate': modified_date
#         })
    
#     return pd.DataFrame(data)

# location_df = generate_location_data(LOCATION_START_ID,LOCATION_END_ID)
# # print(location_df.to_string())

# restaurant_df = generate_restaurant_data(RESTAURANT_START_ID,RESTAURANT_END_ID, location_df)
# # print(restaurant_df.to_string())


# menu_df = generate_menu_data(MENU_START_ID,MENU_END_ID, restaurant_df)
# # print(menu_df.to_string())

# customer_df = generate_customer_data(CUSTOMER_START_ID,CUSTOMER_END_ID)
# # print(customer_df.to_string())

# customer_address_df = generate_customer_address_data(CUSTOMER_ADDRESS_START_ID, CUSTOMER_ADDRESS_END_ID,customer_df)
# # print(customer_address_df.to_string())

# loginaudit_df = generate_login_audit_data(CUSTOMER_LOGIN_AUDIT_START_ID,CUSTOMER_LOGIN_AUDIT_END_ID, customer_df)
# # print(loginaudit_df.to_string())

# # order_df=generate_orders_data(ORDER_START_ID,ORDER_END_ID, customer_df, restaurant_df)
# # print(order_df.to_string())


# delivery_agent_df = generate_delivery_agent_data(DELIVERY_AGENT_START_ID,DELIVERY_AGENT_END_ID,location_df)
# # print(delivery_agent_df.to_string())


# # location_df.to_csv('data/location.csv', index=False)
# # restaurant_df.to_csv('data/restaurant.csv', index=False)
# # menu_df.to_csv('data/menu.csv', index=False)
# # customer_df.to_csv('data/customer.csv', index=False)




# ''' 

# Note :- Customer Adress tabel ma start id and end id aapvani jarur nathi because customer 20 hoi and adress ma 30
# ni limit rakhi  hoi to may be evu thai sake koi customer ne adress na bhi male using start_id and end id  


# '''