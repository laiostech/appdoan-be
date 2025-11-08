# MINIO Guide
docker run -p 9000:9000 -p 9001:9001 --name minio1 -v D:\minio\data:/data -e "MINIO_ROOT_USER=CHIENDEPTRAI" -e "MINIO_ROOT_PASSWORD=CHIENDEPTRAI" quay.io/minio/minio server /data --console-address ":9001"

python manage.py add_default_data - Tạo Đại đội 12 (ID='1')
python manage.py create_sample_data - Tạo 3 chiến sỹ
# run app for native
