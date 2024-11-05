import boto3
from botocore.exceptions import ClientError
import time

ACL_TYPES = ["private", "public-read", "public-read-write", "authenticated-read", "bucket-owner-full-control"]
LOCATIONS = ["ap-south-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "sa-east-1", "us-east-1", "us-east-2", "us-west-1", "us-west-2"]

class S3Bucket:
    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)
        

    def check_bucket(self):
        if not self.bucket_exists(self.bucket_name):
            response = input("This bucket does not exist, create it? (y/n): ")
            if response == 'y':
                self.create_bucket(self.bucket_name)
                #Ensures a valid bucket is loaded into the bucket var
                self.bucket = self.s3.Bucket(self.bucket_name)
            else:
                exit()


    def print_menu(self):
        print("\nMENU\n1 - Create Bucket\n2 - Delete Bucket\n3 - List Buckets\n4 - Search Bucket\n5 - List Bucket Objects\n6 - Download File (Current Bucket)\n7 - Upload Object\n8 - Delete Object\n9 - Open Bucket\n10 - Current Bucket\n0 - Close Application")

    def core_loop(self):
        entry = True

        while entry != 0:
            self.print_menu()
            entry = int(input("\n\nEntry: "))
            match entry:
                case 1:
                    print("Create Bucket")
                    self.create_bucket(input("Enter a GLOBALLY UNIQUE name for the new bucket: "))
                case 2:
                    print("Delete Bucket")
                    self.delete_bucket()
                case 3:
                    print("List Buckets")
                    self.list_buckets()
                case 4:
                    print("Search Bucket")
                    self.search_bucket()
                case 5:
                    print("List Bucket Objects")
                    self.list_bucket_objects()
                case 6:
                    print("Download File")
                    self.download_file()
                case 7:
                    print("Upload Object")
                    self.upload_object()
                case 8:
                    print("Delete Object")
                    self.delete_object()
                case 9:
                    print("Open New Bucket")
                    self.open_bucket()
                case 10:
                    print("Current Bucket Name")
                    self.get_bucket_name()
                case 0:
                    print("Close Application")
                    exit()
                case _:
                    print("Entry must be 0-10")

    def bucket_exists(self, bucket_name):
        try:
            self.s3.meta.client.head_bucket(Bucket = bucket_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] != '404':
                return False
            
    def create_bucket(self, bucket_name):
        ACL_type = input("Enter the ACL Type: ")
        while ACL_type not in ACL_TYPES:
            print("Valid ACL types are: ", ACL_TYPES)
            ACL_type = input("Enter the ACL Type: ")

        location = input("Enter the location for the bucket: ")
        while location not in LOCATIONS:
            print("Valid ACL types are: ", LOCATIONS)
            location = input("Enter the location for the bucket: ")
        try:
            self.s3.create_bucket(
                Bucket = bucket_name,
                ACL = ACL_type,
                CreateBucketConfiguration = {
                    'LocationConstraint':location
                }
            )
        except:
            print("An error occured when creating the bucket. Reminder bucket names must be GLOBALLY UNIQUE")
        if self.bucket_exists(bucket_name):
            print("Bucket Successfully Created")

    def open_bucket(self):
        bucket_name = input("Enter the name of the bucket to open: ")
        try:
            if self.bucket_exists(bucket_name):
                self.bucket_name = bucket_name
                self.bucket = self.bucket = self.s3.Bucket(bucket_name)
                print(f"Opened {self.bucket_name}")
                #list bucket contents
        except:
            print("Error openning the new bucket. Check bucket name.")

    def list_bucket_objects(self):
        print("Bucket Objects: \n")
        for object in self.bucket.objects.all():
            print(object.key)
        time.sleep(2)

    def search_bucket(self):
        search_term = input(f"Search {self.bucket_name} : ")
        found = False
        for object in self.bucket.objects.filter(Prefix = search_term):
            print(object.key)
            found = True
        if found == False:
            print("Item(s) not found")
        time.sleep(2)
    
    def download_file(self):
        print(f"{self.bucket_name} Objects: ")
        self.list_bucket_objects()
        file_name = input("Enter the name of the file to be downloaded: ")
        download_name = input("Download as: ")
        try:
            object = self.s3.Object(self.bucket_name, file_name)
            object.download_file(download_name)
            print(f"{file_name} successfully downloaded")
        except:
            print("File could not be downloaded, check file name and extention")

    def list_buckets(self):
        try:
            buckets = self.s3.meta.client.list_buckets()
            for bucket in buckets['Buckets']:
                print(bucket['Name'])
        except:
            print("An error occured when fetching the buckets.")
        time.sleep(2)
        
    def get_bucket_name(self):
        print(self.bucket_name)

    def delete_object(self):
        obj = input("Enter the name of the object to be delete: ")
        try:
            response = self.s3.meta.client.delete_object(
                Bucket = self.bucket_name,
                Key = obj
            )
            print(f"{obj} has been deleted")
        except:
            print("An error occured. Check object name or AWS connection.")

    def upload_object(self):
        obj = input("Enter the name of the file to be uploaded: ")
        ACL_type = input("Enter the ACL Type: ")
        new_name = input(f"Upload copy of {obj} with the name: ")
        while ACL_type not in ACL_TYPES:
            print("Valid ACL types are: ", ACL_TYPES)
            ACL_type = input("Enter the ACL Type: ")
        try:
            with open(obj, 'rb') as file:
                data = file.read()
        except:
            print("The provided file could not be opened. Check file name.")
        try:
            self.s3.meta.client.put_object(
                ACL = ACL_type,
                Bucket = self.bucket_name,
                Body = data,
                Key = new_name
        )
            print(f"\nUploaded {obj} as {new_name}")
        except:
            print("An error occured when uploading the file.")
    
    def delete_bucket(self):
        entry = input(f"Are you sure that you want to delete the {self.bucket_name} bucket? (y/n): ")
        if entry == 'y':
            entry = input(f"Enter the bucket name ({self.bucket_name}) to confirm deletion: ")
            if entry == self.bucket_name:
                for object in self.bucket.objects.all():
                    object.delete()
                for version in self.bucket.object_versions.all():
                    version.delete()        

                self.bucket.delete()
                print(f"Bucket {self.bucket_name} deleted\n")
                self.open_bucket()
            else:
                print("Bucket deletion aborted (name not entered correctly)")



def main():
    bucket = input("Enter a bucket to open or create: ")
    bucket = S3Bucket(bucket)
    bucket.check_bucket()
    bucket.core_loop()


if __name__ == '__main__':
    main()
    
