# Автоматизированное определение тубулита на основании критериев Banff-классификации патологии аллотрансплантата почки

Banff-классификация — это международная консенсусная классификация для отчетности о биопсиях трансплантатов твердых органов (в данном случае почки).
Тубулит —  состояние при котором в базолатеральной части эпителия почечных канальце находятся мононуклеарные клетки.
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182348.png)

### Гипотеза нашего исследования:
Анализ скан-изображений гистологических препаратов пункционных биоптатов трансплантированных почек на основе глубокого обучения позволит сегментировать тубулит на основе Banff-классификации с оценкой Recall и Precision не менее 0,7.

### Проблема/Актуальность:
Ручной подсчет тубулита требует больших затрат времени и ресурсов у патологов. Он подвержен субъективной оценке, так как имеет сложности из-за изменчивости канальцев по форме, размеру, ориентации и различных форм воспалительных клеток. Автоматизированное определение тубулита может ускорить процесс написания гистологического заключения, минимизируя субъективизм, способствуя ускорению принятия решения в тактике лечения пациента после трансплантации почки.

### Сложнсть и сопоставление с данными литературы: 
В мировой практике нет достаточного количества работ по сегментации/детекции тубулита как морфологического признака. Отчасти это объясняется сложной вариацией форм канальцев, активность воспаления из-за чего нарушаются границы исследуемого объекта, отсуствие нормализации окраски гистологических препаратов и сложность определения мононуклеарных клеток с точной локализацией. Сопоставляя данные литературы мы можем увидеть, что при сегментации тубулита лучшие показатели Dice-coefficient составляет 0.30, что несомненно низко. В нашей работе мы попробуем найти подход для улучшения метрики или применения иных методов для прикладного применения в помощи врачам патологам.

### Подготовка датасета происходила в откытом програмном обеспечении QuPath, предназначенной для работы с биомедицинскими (гистологическими) цифровыми изображениями. 
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182453.png)

Мы экспортировали размеченные данные в виде плиток 512 х 512 px и соответсвующих им бинарные/мультиклассовые маски. С учетом небольшого количества данных производиталь аугментация данных с помощью библиотеки Albumentation (https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Augmentation/Augmen_Tubulitis.ipynb) - ноутбук с агументацией.

### Первая попытка бинарной сегментации тубулита была произведена на архитектуре U-Net&ResNet101 
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182540.png)
(https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Binary_segmentation_Tubulitis/Segmentation_Tubulitis_SMP_UnetPlus_ipynb_.ipynb)

### Вторая попыта была произведена на архитектуре YOLOv8
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182618.png)

(https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Binary_segmentation_Tubulitis/Detection_Tubulitis_YoloV8_ipynb_.ipynb)

### Третья попытка - пробуем сегментировать все канальцы без дифференцировки на тубулит и нормальные.
![Image alt] (https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182640.png)

Ноутбук - (https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/All_tubules_segmentation/PyTorch_Ligh_Multi.ipynb)

### Четвертая попытка - поиск альтернатив - задействование трансформеров с учетом их обобщающих алгоритмов
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182704.png)

![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182726.png)

При некотором обучении удалось добиться метрик близких к необходимым, на валидационной выборке Recall&Precision 0.663/0.581 соответсвенно.

### Необходимость изменения подхода
В связи с возникшими трудностями был предпринят иной подход. Провести инстанс сегментацию канальцев всех (хорошие метрики позволяли нам это сделать) и провести детекцию мононуклеарных клеток. Затем оставить только те полигоны предсказаний канальцев, которые пересекались бы с детектированными мононуклеарными клетками. Тем самым создав финальную бинарную маску тубулита.

Вот как выглядел принцип работы каскада моделей:
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182744.png)







