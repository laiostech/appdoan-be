-- SQL Insert script cho hệ thống quản lý đại đội
-- Chạy script này sau khi đã tạo tables với migrations

-- Xóa dữ liệu cũ (nếu có)
DELETE FROM military_management_soldier;
DELETE FROM military_management_company;

-- Insert đại đội
INSERT INTO military_management_company (id, name, description, created_at, updated_at) VALUES
('company-01', 'Đại đội 1', 'Đại đội số 1 - Đại đội chủ lực', NOW(), NOW()),
('company-02', 'Đại đội 2', 'Đại đội số 2 - Đại đội phụ trợ', NOW(), NOW());

-- Insert chiến sỹ đại đội 1
INSERT INTO military_management_soldier (
    id, company_id, full_name, birth_date, soldier_rank, soldier_position, place_work,
    join_union_party_date, ethnicity, education, 
    religion, hometown, father_name, mother_name, phone_number, 
    created_at, updated_at
) VALUES 
(
    'soldier-01', 'company-01', 'Phạm Quốc Tường', '2000-05-01', '2', 'bt', 'bCo1',
    '2015-03-26', 'Kinh', 'ĐH',
    'Không', 'Xóm 2, xã Hùng Châu, Nghệ An', 'Phạm Văn Cần', 'Dặng Thị Dung', '0974934126',
    NOW(), NOW()
),
(
    'soldier-02', 'company-01', 'Nguyễn Đình Quang', '2005-04-07', 'H2', 'kđt', 'Kđ1',
    NULL, 'Kinh', '9/12',
    'Không', 'Quảng Phú, Thanh Hóa', 'Nguyễn Đình Cảnh', 'Lê Thị Thảo / Lò Thị Chung', '0372442421',
    NOW(), NOW()
),
(
    'soldier-03', 'company-01', 'Lê Văn Vũ', '2003-11-30', 'B2', 'cs', 'Kđ1',
    NULL, 'Kinh', 'CĐ',
    'Không', 'Hải Bình, Quãng Trị', 'Lê Văn Bảy', 'Lê Thị Phương Nhị', '0966761946',
    NOW(), NOW()
),
(
    'soldier-04', 'company-01', 'Phan Thế Duẩn', '2006-08-10', 'B2', 'cs', 'Kđ1',
    NULL, 'Kinh', '9/12',
    'Không', 'Sầm Sơn, Thanh Hóa', 'Phan Thế Thế (mất)', 'Nguyễn Thị Hà', '0339187430',
    NOW(), NOW()
),
(
    'soldier-05', 'company-01', 'Lê Đức Chung', '2006-05-12', 'B2', 'cs', 'Kđ1',
    NULL, 'Kinh', '12/12',
    'Không', 'Sầm Sơn, Thanh Hóa', 'Lê Đức Thịnh', 'Lê Thị Vân', '0399608874',
    NOW(), NOW()
);

-- Insert chiến sỹ đại đội 2
INSERT INTO military_management_soldier (
    id, company_id, full_name, birth_date, soldier_rank, soldier_position, place_work,
    join_union_party_date, ethnicity, education, 
    religion, hometown, father_name, mother_name, phone_number, 
    created_at, updated_at
) VALUES 
(
    'soldier-06', 'company-02', 'Trần Văn Đức', '2004-03-15', 'B1', 'cs', 'K2',
    '2020-05-10', 'Kinh', 'CĐ',
    'Không', 'Hà Nội', 'Trần Văn An', 'Nguyễn Thị Bình', '0912345678',
    NOW(), NOW()
),
(
    'soldier-07', 'company-02', 'Hoàng Minh Tuấn', '2005-07-20', 'B2', 'cs', 'K2',
    '2021-08-15', 'Kinh', '12/12',
    'Không', 'TP. Hồ Chí Minh', 'Hoàng Minh Khải', 'Lê Thị Mai', '0987654321',
    NOW(), NOW()
);

-- Kiểm tra dữ liệu đã insert
SELECT 'COMPANIES' as table_name, COUNT(*) as count FROM military_management_company
UNION ALL
SELECT 'SOLDIERS' as table_name, COUNT(*) as count FROM military_management_soldier;

-- Hiển thị dữ liệu mẫu
SELECT 
    c.name as company_name,
    s.full_name,
    s.birth_date,
    CONCAT(s.soldier_rank, '/', s.soldier_position) as rank_position,
    s.place_work,
    s.phone_number
FROM military_management_company c
LEFT JOIN military_management_soldier s ON c.id = s.company_id
ORDER BY c.name, s.full_name; 