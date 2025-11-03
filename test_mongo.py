import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from alumeee import YourModel

def test_mongo():
    # Try fetching all objects
    objs = YourModel.objects.all()
    print("Objects in MongoDB:", objs)

    # Try creating a test object (adjust fields accordingly)
    obj = YourModel(field1='test', field2='value')
    obj.save()
    print("Saved object:", obj)

if __name__ == "__main__":
    test_mongo()
