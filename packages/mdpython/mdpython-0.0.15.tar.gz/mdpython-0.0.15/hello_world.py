from mdpython.datautils import jsonutil

json_data = {
    "data": [
        {
            "name": "John",
            "age": 30,
            "car": {
                "make": "Toyota",
                "model": "Camry"
            },
            "colors": ["red", "blue", "green"]
        }, {
            "name": "Sheema",
            "age": 25,
            "car": {
                "make": "Audi",
                "model": "a4",
                "dimension": [5000, 1850, 1433]
            },
            "colors": ["blue", "yellow"]
        }, {
            "name": "Bruce",
            "car": {
                "make": "Ford"
            }
        }
    ]
}

print(jsonutil.find_values_by_key(json_data, "colors"))
print(jsonutil.search(json_data, "blue"))