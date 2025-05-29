INSERT INTO user (first_name, last_name, email, mobile, gender, country, state, password_hash, transaction_pin, username, referral_code, referred_by, is_admin, user_id, profile_picture_id, created_at)
VALUES ('Alice', 'Smith', 'alice.smith@example.com', '+17540046279', 'Female', 'USA', 'California', '4liga582', '3894', 'alicesmith', NULL, NULL, NULL, '2cb80244-3f12-4281-92b4-1c7b59faa74b', '2cb80244-3f12-4281-92b4-1c7b59faa74b', '2025-05-28 13:32:16'),
('Bob', 'Johnson', 'bob.johnson@example.com', '+13312445829', 'Female', 'Canada', 'Ontario', '6rajqog7', '4486', 'bobjohnson', NULL, NULL, NULL, '8349f302-dbdc-4676-a84d-a065d5f29c34', '8349f302-dbdc-4676-a84d-a065d5f29c34', '2025-05-28 13:32:16'),
('Charlie', 'Williams', 'charlie.williams@example.com', '+13165745001', 'Female', 'UK', 'London', 'ifl3r3j3', '6000', 'charliewilliams', NULL, NULL, NULL, '6553ebd1-a1c6-46af-a000-004d78e9635f', '6553ebd1-a1c6-46af-a000-004d78e9635f', '2025-05-28 13:32:16'),
('Diana', 'Brown', 'diana.brown@example.com', '+11451221955', 'Male', 'Australia', 'Sydney', 'fybz8d3r', '8113', 'dianabrown', NULL, NULL, NULL, 'b9fc2372-8437-4f6e-a619-457ece5ff9c4', 'b9fc2372-8437-4f6e-a619-457ece5ff9c4', '2025-05-28 13:32:16'),
('Ethan', 'Jones', 'ethan.jones@example.com', '+14288671337', 'Female', 'Germany', 'Bavaria', 'c3izn6vn', '3657', 'ethanjones', NULL, NULL, NULL, '4176f86a-0a48-45c5-8a24-ea061096271f', '4176f86a-0a48-45c5-8a24-ea061096271f', '2025-05-28 13:32:16'),
('Fiona', 'Garcia', 'fiona.garcia@example.com', '+12025333318', 'Female', 'India', 'Delhi', 'h6njhtqb', '9913', 'fionagarcia', '7ficj0v7', '4176f86a-0a48-45c5-8a24-ea061096271f', NULL, '5a730d20-6fd4-4aec-b0a1-5e189e2b3c5b', '5a730d20-6fd4-4aec-b0a1-5e189e2b3c5b', '2025-05-28 13:32:16'),
('George', 'Miller', 'george.miller@example.com', '+18958540091', 'Male', 'Brazil', 'São Paulo', '5e1lpzyk', '8096', 'georgemiller', 'l4a096oi', 'b9fc2372-8437-4f6e-a619-457ece5ff9c4', NULL, '3ba2f8d8-d1ba-43c9-8615-059ca29b04a1', '3ba2f8d8-d1ba-43c9-8615-059ca29b04a1', '2025-05-28 13:32:16'),
('Hannah', 'Davis', 'hannah.davis@example.com', '+16051423598', 'Female', 'France', 'Île-de-France', 'aprs2yj2', '2142', 'hannahdavis', 'gnsxmiys', '6553ebd1-a1c6-46af-a000-004d78e9635f', NULL, '5880d48a-0d72-4975-875b-444b1faaf391', '5880d48a-0d72-4975-875b-444b1faaf391', '2025-05-28 13:32:16'),
('Ian', 'Rodriguez', 'ian.rodriguez@example.com', '+15525346320', 'Male', 'Japan', 'Tokyo', '6zlgyve3', '6183', 'ianrodriguez', 'h3fcznc9', '2cb80244-3f12-4281-92b4-1c7b59faa74b', NULL, '62e05ad8-6e6c-4ee4-9905-50ef776d50b7', '62e05ad8-6e6c-4ee4-9905-50ef776d50b7', '2025-05-28 13:32:16'),
('Jenna', 'Martinez', 'jenna.martinez@example.com', '+16965985201', 'Female', 'Nigeria', 'Lagos', 'qm8r8x0w', '9506', 'jennamartinez', 'iw29egxu', '4176f86a-0a48-45c5-8a24-ea061096271f', NULL, '452fa2ca-f317-43a3-b9c8-34bc639385ed', '452fa2ca-f317-43a3-b9c8-34bc639385ed', '2025-05-28 13:32:16');


INSERT INTO user (
  first_name, last_name, email, mobile, gender, country, state,
  password_hash, transaction_pin, username, referral_code, referred_by,
  is_admin, user_id, profile_picture_id, created_at
) VALUES
('Ada', 'Okonkwo', 'ada.okonkwo@example.com', '08012345678', 'Female', 'Nigeria', 'Enugu',
 'b7xk2d3p', '1234', 'AdaOkonkwo', NULL, NULL, NULL,
 'a1c3f001-12d4-4a56-b789-111c2b3a4567', 'a1c3f001-12d4-4a56-b789-111c2b3a4567', NOW()),

('John', 'Doe', 'john.doe@example.com', '08023456789', 'Male', 'USA', 'California',
 'h9k2m8p1', '5678', 'JohnDoe', NULL, NULL, NULL,
 'b2d4f002-23e5-5b67-c890-222d3c4b5678', 'b2d4f002-23e5-5b67-c890-222d3c4b5678', NOW()),

('Chinedu', 'Eze', 'chinedu.eze@example.com', '08034567890', 'Male', 'Nigeria', 'Lagos',
 'a1b2c3d4', '7890', 'ChineduEze', 'k3fj2nmv', 'a1c3f001-12d4-4a56-b789-111c2b3a4567', NULL,
 'c3e5g003-34f6-6c78-d901-333e4d5c6789', 'c3e5g003-34f6-6c78-d901-333e4d5c6789', NOW()),

('Maria', 'Gonzalez', 'maria.g@example.com', '08045678901', 'Female', 'Mexico', 'Jalisco',
 'z8y7x6w5', '3456', 'MariaGonzalez', 'k4lj8pqx', 'b2d4f002-23e5-5b67-c890-222d3c4b5678', NULL,
 'd4f6h004-45g7-7d89-e012-444f5e6d7890', 'd4f6h004-45g7-7d89-e012-444f5e6d7890', NOW()),

('Fatima', 'Abubakar', 'fatima.abubakar@example.com', '08056789012', 'Female', 'Nigeria', 'Kano',
 'n6m5l4k3', '9012', 'FatimaAbubakar', NULL, NULL, NULL,
 'e5g7i005-56h8-8e90-f123-555g6f7e8901', 'e5g7i005-56h8-8e90-f123-555g6f7e8901', NOW()),

('William', 'Smith', 'william.smith@example.com', '08067890123', 'Male', 'UK', 'London',
 'q3w2e1r0', '1122', 'WilliamSmith', 'k8zj2qmx', 'c3e5g003-34f6-6c78-d901-333e4d5c6789', NULL,
 'f6h8j006-67i9-9f01-a234-666h7g8f9012', 'f6h8j006-67i9-9f01-a234-666h7g8f9012', NOW()),

('Ngozi', 'Nwosu', 'ngozi.nwosu@example.com', '08078901234', 'Female', 'Nigeria', 'Abia',
 'l0k9j8h7', '3344', 'NgoziNwosu', NULL, NULL, NULL,
 'g7i9k007-78j0-0g12-b345-777i8h9g0123', 'g7i9k007-78j0-0g12-b345-777i8h9g0123', NOW()),

('Ahmed', 'Ibrahim', 'ahmed.ibrahim@example.com', '08089012345', 'Male', 'Egypt', 'Cairo',
 'm1n2b3v4', '5566', 'AhmedIbrahim', 'k9mp4qzx', 'f6h8j006-67i9-9f01-a234-666h7g8f9012', NULL,
 'h8j0l008-89k1-1h23-c456-888j9i0h1234', 'h8j0l008-89k1-1h23-c456-888j9i0h1234', NOW()),

('Tosin', 'Ola', 'tosin.ola@example.com', '08090123456', 'Male', 'Nigeria', 'Oyo',
 'x1c2v3b4', '7788', 'TosinOla', NULL, NULL, NULL,
 'i9k1m009-90l2-2i34-d567-999k0j1i2345', 'i9k1m009-90l2-2i34-d567-999k0j1i2345', NOW()),

('Lucy', 'Chen', 'lucy.chen@example.com', '08101234567', 'Female', 'China', 'Beijing',
 'r4e5t6y7', '9900', 'LucyChen', 'k1mz3plq', 'd4f6h004-45g7-7d89-e012-444f5e6d7890', NULL,
 'j0l2n010-a1m3-3j45-e678-000l1k2j3456', 'j0l2n010-a1m3-3j45-e678-000l1k2j3456', NOW());
