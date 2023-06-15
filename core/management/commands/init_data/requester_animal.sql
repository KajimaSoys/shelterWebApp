INSERT INTO public.core_animal
(id, name, animal_type, breed, age, gender, weight, health_status, description, shelter_id, "order", status, created_at)
VALUES
(1, 'Пушистик', 'Кот', 'Персидская', 2, 'female', 4.5, 'Отличное', '<p>Игривая и дружелюбная</p>', 1, 1, 'in_shelter', '2023-05-15'),
(2, 'Рекс', 'Собака', 'Немецкая овчарка', 3, 'male', 30, 'Хорошее', '<p>Энергичный и верный</p>', 1, 2, 'in_shelter', '2023-05-15'),
(3, 'Белла', 'Кот', 'Сиамская', 4, 'female', 4, 'Хорошее', '<p>Спокойная и нежная</p>', 1, 3, 'in_shelter', '2023-05-15'),
(4, 'Макс', 'Собака', 'Лабрадор Ретривер', 1, 'male', 25, 'Отличное', '<p>Очень активный и дружелюбный</p>', 1, 4, 'in_shelter', '2023-05-15'),
(5, 'Тигр', 'Кот', 'Бенгальская', 3, 'male', 5, 'Отличное', '<p>Красивый и игривый</p>', 1, 5, 'in_shelter', '2023-05-15'),
(6, 'Люси', 'Собака', 'Бигль', 2, 'female', 20, 'Хорошее', '<p>Любящая и прекрасная с детьми</p>', 1, 6, 'in_shelter', '2023-05-15'),
(7, 'Молли', 'Кот', 'Мейн кун', 5, 'female', 6, 'Good', '<p>Quiet and independent</p>', 1, 7, 'in_shelter', '2023-05-15'),
(8, 'Роки', 'Собака', 'Ротвеллер', 4, 'male', 40, 'Good', '<p>Protective and loyal</p>', 1, 8, 'in_shelter', '2023-05-15'),
(9, 'Смоки', 'Кот', 'Русская голубая', 2, 'male', 4.5, 'Excellent', '<p>Intelligent and gentle</p>', 1, 9, 'in_shelter', '2023-05-15'),
(10, 'Дейзи', 'Собака', 'Долматинец', 1, 'female', 18, 'Excellent', '<p>Active and outgoing</p>', 1, 10, 'in_shelter', '2023-05-15'),
(11, 'Луна', 'Кот', 'Рэгдолл', 3, 'female', 4, 'Good', '<p>Loving and calm</p>', 1, 11, 'in_shelter', '2023-05-15'),
(12, 'Джек', 'Собака', 'Коли', 1, 'male', 15, 'Excellent', '<p>Intelligent and energetic</p>', 1, 12, 'in_shelter', '2023-05-15'),
(13, 'Оливер', 'Кот', 'Британская корткошерстная', 4, 'male', 5.5, 'Good', '<p>Easygoing and affectionate</p>', 1, 13, 'in_shelter', '2023-05-15'),
(14, 'Чарли', 'Собака', 'Золотой Ретривер', 2, 'male', 30, 'Excellent', '<p>Friendly and loyal</p>', 1, 14, 'in_shelter', '2023-05-15'),
(15, 'Хлоя', 'Кот', 'Шотландец', 3, 'female', 4, 'Good', '<p>Playful and loving</p>', 1, 15, 'in_shelter', '2023-05-15');

SELECT setval('public.core_animal_id_seq', (SELECT MAX(id) from public.core_animal));