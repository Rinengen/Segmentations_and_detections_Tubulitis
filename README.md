# Автоматизированное определение тубулита на основании критериев Banff-классификации патологии аллотрансплантата почки.

Banff-классификация — это международная консенсусная классификация для отчетности о биопсиях трансплантатов твердых органов (в данном случае почки).

Тубулит —  состояние при котором в базолатеральной части эпителия почечных канальце находятся мононуклеарные клетки (отмечены стрелочками на рисунке ниже).

![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182348.png)

### Гипотеза нашего исследования:
Анализ скан-изображений гистологических препаратов пункционных биоптатов трансплантированных почек на основе глубокого обучения позволит сегментировать тубулит на основе Banff-классификации с оценкой Recall и Precision не менее 0,7.

### Проблема/Актуальность:
Ручной подсчет тубулита требует больших затрат времени и ресурсов у патологов. Он подвержен субъективной оценке, так как имеет сложности из-за изменчивости канальцев по форме, размеру, ориентации и различных форм воспалительных клеток. Автоматизированное определение тубулита может ускорить процесс написания гистологического заключения, минимизируя субъективизм, способствуя ускорению принятия решения в тактике лечения пациента после трансплантации почки.

### Сложность и сопоставление с данными литературы: 
В мировой практике нет достаточного количества работ по сегментации/детекции тубулита как морфологического признака. Отчасти это объясняется сложной вариацией форм канальцев, активность воспаления из-за чего нарушаются границы исследуемого объекта, отсуствие нормализации окраски гистологических препаратов и сложность определения мононуклеарных клеток с точной локализацией. Сопоставляя данные литературы мы можем увидеть, что при сегментации тубулита лучшие показатели Dice-coefficient составляет 0.30, что несомненно низко. В нашей работе мы попробуем найти подход для улучшения метрики или применения иных методов для прикладного применения в помощи врачам патологам.

### Подготовка датасета происходила в откытом програмном обеспечении QuPath, предназначенной для работы с биомедицинскими (гистологическими) цифровыми изображениями. 
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182453.png)

Мы экспортировали размеченные данные в виде плиток 512 х 512 px и соответсвующих им бинарные/мультиклассовые маски. С учетом небольшого количества данных производиталь аугментация данных с помощью библиотеки Albumentation 

[Аугментация данных](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Augmentation/Augmen_Tubulitis.ipynb)

### Первая попытка бинарной сегментации тубулита была произведена на архитектуре U-Net&ResNet101 
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182540.png)

[U-Net_binary_segmentation](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Binary_segmentation_Tubulitis/Segmentation_Tubulitis_SMP_UnetPlus_ipynb_.ipynb)

### Вторая попыта была произведена на архитектуре YOLOv8
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182618.png)

[YOLOv8_binary_segmentation](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Binary_segmentation_Tubulitis/Detection_Tubulitis_YoloV8_ipynb_.ipynb)

### Третья попытка - пробуем сегментировать все канальцы без дифференцировки на тубулит и нормальные.
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182640.png)

[All_tubuli_segmentation](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/All_tubules_segmentation/PyTorch_Ligh_Multi.ipynb)

### Четвертая попытка - поиск альтернатив - задействование трансформеров с учетом их обобщающих алгоритмов
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182704.png)

![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182726.png)

[SegFormer_segmentation](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/SegFormer_binary_segmentation/segfrom.ipynb)

При некотором обучении удалось добиться метрик близких к необходимым, на валидационной выборке Recall&Precision 0.663/0.581 соответсвенно.

### Необходимость изменения подхода
В связи с возникшими трудностями был предпринят иной подход. Провести инстанс сегментацию канальцев всех (хорошие метрики позволяли нам это сделать) и провести детекцию мононуклеарных клеток. Затем оставить только те полигоны предсказаний канальцев, которые пересекались бы с детектированными мононуклеарными клетками. Тем самым создав финальную бинарную маску тубулита.

Вот как выглядел принцип работы каскада моделей:
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182744.png)

### Проблемы сегментации на каскаде
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182802.png)

На рисунке мы видим, что сегментация канальцев, а именно границ канальцев, не всегда имеет достаточной точности. Анализируя результаты, можно утверждать, что при различных вариантах интенсивности окрашивания, наличия воспалительных или атрофических изменений в канальцах мы получаем различные, и порой неудовлетворительные результаты сегментации. Отсутствие отчетливо сегментированных границ канальцев не позволяет сопоставить пересечение сегментированного канальца и детектированной мононуклеарной клетки, что снижает предсказательную мощность моделей.

### Таблица результатов
![Image alt](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Visualisation/Snapshot_240624182823.png)

### Оценка межэкспертной согласованности
Каскад моделей оценен на валидационном наборе данных с заключениями патолога по стадиям тубулита.
Каждый из скан-изображений разбивался на плитки размерами 256х256px, которые в дальнейшем анализировались нашим каскадом моделей и специально разработанным алгоритмом. В основе алгоритма задавался следующий сценарий:  поиск количества пересечений  в сегментированном канальце с детектированными мононуклеарными клетками, тем самым создавая лист с количеством клеток в каждом найденном канальце с пересечении; оставляем самое большое количество пересечений на плитке;  используем условие присвоения стадии тубулита, согласно классификация Банффа патологии почечного трансплантата [2]; в итоге  плитке  присваивается стадия тубулита; во время работы алгоритма создается список стадий тубулита из всех плиток WSI и  заключение по скан-изображению выносится путем усреднения предсказаний. 

[Пример работы каскада](https://github.com/Rinengen/Segmentations_and_detections_Tubulitis/blob/main/Essemble/YOLO_Essemble.ipynb)

В итоге мы получаем список предсказаний модели и оценок патолога по стадии тубулита для скан-изображения. Полученный список использовался для измерения уровня согласия между моделью и патологом с помощью коэффициента Каппа Коэна, который составил 0.62 (сильная, но не применимая для медицинских заключений).


### Выводы по работе
В данном исследовании мы разработали модель для сегментации тубулита в скан-изображениях гистологических препаратов трансплантата почки, окрашенных по методу H&E (H-DAB). Наши основные результаты заключаются в том, что с помощью глубокого обучения возможно произвести сегментацию тубулита по критериям Банфф, однако точность классической семантической сегментации остается низкой, что соотносится с данными литературы. Возможные причины кроются в сложном целевом признаке: трудность дифференцировки тубулита от нормальных канальцев, сложность дифференцировки мононуклеарных клеток с ядрами эпителиальных клеток. Мной была исследовано три архитектуры нейросети для решения данной задачи: U-Net, YOLOv8, SegFormer. Наиболее перспективно показала себя архитектура трансформера SegFormer с метрикой Recall 0.633, Precision 0.543, F1-Score 0,61 на валидационном наборе данных, и 0.576, 0.401, 0.416 соответственно на тестовом наборе. Метод, основанный на каскаде моделей, показал улучшенные результаты: Recall 0.544, Presision – 0.498, IoU - 0.247. Ограничениями каскада моделей стала плохая сегментация патологических канальцев на фоне воспалительных изменений, что не позволяет находить пересечения детектированных объектов на базолатеральной мембране (границе объектов) в некоторых случаях. Модель была проверена на валидационном датасете, которая содержала экспертные оценки стадии тубулита, присвоенные врачом-патологом. Оценка согласия между патологом и автоматизированным определением стадии тубулита при подсчете коэффициента Каппа Коэна составила 0.62. Несмотря на сильное согласие между двумя методами, для медицинских исследований требуется результат близкий к полному согласий результатов. Кроме того, для повышения Recall в определении стадии тубулита между 0 и 1 стадией, был оставлен порог вероятности в 0.3, учитывая долю ложноположительных и ложноотрицательных предсказаний. Данный порог позволяет сделать результаты работы модели удобными для врача, когда необходимо понимать, где имеется высокий риск патологии, имея precision и recall для стадии 0 – 0.92/0.71, для стадии 1 -0.73/0.95, для стадии 2 – 1.0/0.67. 

Подтвержденная научная гипотеза об использовании глубокого обучения для определения тубулита, несмотря на несовпадение с первоначальными ожиданиями, открывает перспективы для корректировки нашего исследования. Низкая точность выявления тубулита на собственном датасете объясняется сложностью целевого признака и ограниченным объемом выборки. Исходя из результатов исследования, возможные пути решения проблемы рассматриваются в контексте различных стратегий.

Один из вариантов – это маркировка всех канальцев на класс "нормальный" или "патологический", что позволит избежать ложных срабатываний и повысить точность определения тубулита. Другим немаловажным ограничением является отсутствие стандартизации окрашивания гистологических снимков. Требуется длительная и кропотливая работа над поиском нормализации изображений, даже в разделе окраски H&E, не говоря уже об отличных методах окрашивания. Чтобы преодолеть выявленные проблемы, предлагается ряд стратегических действий. Во-первых, расширение обучающей выборки для улучшения обобщающей способности моделей. Это может быть достигнуто путем сбора дополнительных данных и стандартизации процесса их подготовки. Во-вторых, исследовать возможности использования более сложных архитектур нейронных сетей, включая каскадные модели на основе трансформеров.

Необходимо отметить, что даже при низкой предсказательной точности в определении тубулита, методология исследования позволяет обучить модель на подготовленных датасетах для точного выявления всех канальцев в биопсии почки. Это свидетельствует о успешности нашего исследования, поскольку модели, обученные на таких датасетах, демонстрируют высокие результативные метрики, такие как Recall – 0.74, Precision – 0.92, IoU – 0.687, и F1-Score – 0.806.

В результате выполненной работы достигнуты следующие результаты: освоена методология работы по сегментации и детекции объектов на гистологических изображениях; получены навыки работы со специальным программным обеспечением для работы с биомедицинскими изображениями (QuPath), с форматами многоканальных гистологических изображений; собрано три датасета (для семантической сегментации тубулита, для инстанстной сегментации канальцев, для детекции лимфоцитов); разработаны скрипты Python для конвертации бинарных масок в формат coco json и yaml; обучены модели на архитектурах U-Net и YOLOv8; разработан каскад моделей YOLOv8 для индивидуальной сегментации канальцев и детекции лимфоцитов с целью определения тубулита; проведен анализ полученных эмпирических результатов; проведены статистические тесты для оценки согласия между ручным и автоматическим заключением по стадии тубулита. 

#### В заключение следует отметить, что полученные нами результаты свидетельствуют о целесообразности использования автоматизированной и воспроизводимой предварительной классификации тубулита в биоптатах почечного аллотрансплантата. Этот подход может улучшить диагностику биопсии аллотрансплантата благодаря взаимодействию компьютера и человека. С практической точки зрения, модель может быть интегрирована в программное обеспечение QuPath для автоматизации аннотирования и сбора больших объемов данных. Это позволит создать цикл обучения-аннотирования, что в свою очередь способствует повышению качества обучения модели. При достижении удовлетворительных метрик, модель будет готова для использования в вынесении патогистологических заключений о тубулите, согласно классификации Банфф. Интеграция искусственного интеллекта в клиническую практику может помочь патологоанатомам принимать обоснованные решения. Это позволит ускорить вынесение патогистологического заключения в клинической практике и улучшить тактику ведения пациентов с целью предотвращения острого почечного отторжения после трансплантации почки.









