from e_mall.models.category import Category 
from e_mall.models.location import Location 
def navbar():
    e_category_order=['Laptops',
        'Cellphones',
        'Gadgets',
        ]
    
    e_categories_by_order=[]
    for cat_value in e_category_order:        
        cat_output = Category.objects.get(name=cat_value)
        e_categories_by_order.append(cat_output)

    category_order=[
        'Clothing',
        'Men',
        'Women',
        'Services',
        'Jobs',
        'Vehicles',
        'Properties',
        'Tools',
        'Products',
        'Entertainment',
        'Books']
    categories_by_order=[]
    for cat_value in category_order:        
        cat_output = Category.objects.get(name=cat_value)
        categories_by_order.append(cat_output)  
   
    return e_categories_by_order, categories_by_order
 
def loco():
    location_order=[
        'Harare',
        'Chitungwiza',
        'Bulawayo',
        'Gweru',
        'Mutare',
        'Rusape',
        'Masvingo',
        'Orania',
	    'Cape Town',
	    'Pretoria',
        'Johannesburg',
	    'Lusaka',
        'Seattle',
        'Texas',
        'California',
        'Manchester',
        'London',
        'Beijing',

        ]
    location_by_order=[]
    for loc_value in location_order:        
        loc_output = Location.objects.get(name=loc_value)
        location_by_order.append(loc_output)

    return location_by_order