class Risk:
    """
    Класс отрисовки потенциального риска
    """
    def __init__(self, width, height):
        """

        """
        self.widht = width
        self.height = height





def draw_risk_object(self):
    print("Init risk")
    # проверка базы данных
    if self.is_there_a_database() == False:
        return
    # Проверка ген.плана
    if self.is_there_a_plan() == False:
        return
    # Проверка наличия объектов
    if self.any_objects_in_data_obj() == False:
        return
    # проверка равенства объектов Эксель и объектов карты
    if self.equality_obj() == False:
        return
    # достаем картинку из БД
    image_data = ''  # переменная хранения blob из базы данных
    path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
    path_str = path_str.replace("/", "//")
    sqliteConnection = sqlite3.connect(path_str)
    cursorObj = sqliteConnection.cursor()
    cursorObj.execute("SELECT * FROM objects")
    plant_in_db = cursorObj.fetchall()
    text = self.plan_list.currentText()
    for row in plant_in_db:
        if str(row[3]) + ',' + str(row[0]) == text:
            image_data = row[2]
    sqliteConnection.execute("VACUUM")
    cursorObj.close()

    if image_data == '':  # значит картинку не получили
        print("нет картинки")
        return
    if self.data_excel.text() == '':
        print("данных из экселя нет")
        return

    # На основе исходной картинки создадим QImage и QPixmap
    qimg = QtGui.QImage.fromData(image_data)
    pixmap = QtGui.QPixmap.fromImage(qimg)
    # создадим соразмерный pixmap_zone и сделаем его прозрачным
    width, height = pixmap.width(), pixmap.height()
    pixmap_zone = QtGui.QPixmap(width, height)
    pixmap_zone.fill(QtGui.QColor(0, 0, 0, 0))
    qimg_zone = pixmap_zone.toImage()

    # сделаем нулевую матрицу по размерам картинки
    zeors_array = np.zeros((width, height))

    excel = eval(self.data_excel.text())
    objects = self.data_obj.values()

    index = 0
    for obj in objects:
        # возьмем масштаб оборудования
        scale_name = float(obj.get("scale_name"))
        # возьмем координаты оборудования
        obj_coord = eval(obj.get("obj_coord"))
        print(f'calc_{obj_coord}')
        # возьмем тип объекта
        obj_type = obj.get("obj_type")
        max_radius = excel[index][-1] * scale_name
        probit = excel[index][0]
        power = self.power_data(max_radius, probit)
        index += 1

        # Определим рамку для поиска риска
        width_min, height_min, width_max, height_max = self.rect_coord_calc(obj_coord, max_radius, width, height)

        if len(obj_coord) > 2:  # координаты можно преобразовать в полигон или линию
            if obj_type == 0:
                # линейн. получим полигон
                obj_coord = self.get_polyline_shapely(obj_coord)
                self.calc_el_zeors_array(width_min, height_min, width_max, height_max,
                                         obj_coord, power, zeors_array, scale_name)
            else:
                # стац. об. получим полигон
                obj_coord = self.get_polygon_shapely(obj_coord)
                # print(obj_coord)
                self.calc_el_zeors_array(width_min, height_min, width_max, height_max,
                                         obj_coord, power, zeors_array, scale_name)
        else:  # не получается полигон, значит точка
            obj_coord = Point(float(obj_coord[0]), float(obj_coord[1]))
            # print(obj_coord)
            self.calc_el_zeors_array(width_min, height_min, width_max, height_max,
                                     obj_coord, power, zeors_array, scale_name)
    print('draw')
    max_el = zeors_array.max()
    for x in range(width):
        for y in range(height):
            if zeors_array[x, y] >= max_el:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 0, 0, 255))
            elif max_el * 0.99 > zeors_array[x, y] >= max_el * 0.98:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 10, 0, 255))
            elif max_el * 0.98 > zeors_array[x, y] >= max_el * 0.97:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 20, 0, 255))
            elif max_el * 0.97 > zeors_array[x, y] >= max_el * 0.96:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 30, 0, 255))
            elif max_el * 0.96 > zeors_array[x, y] >= max_el * 0.95:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 40, 0, 255))
            elif max_el * 0.95 > zeors_array[x, y] >= max_el * 0.94:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 50, 0, 255))
            elif max_el * 0.94 > zeors_array[x, y] >= max_el * 0.93:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 60, 0, 255))
            elif max_el * 0.93 > zeors_array[x, y] >= max_el * 0.92:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 70, 0, 255))
            elif max_el * 0.92 > zeors_array[x, y] >= max_el * 0.91:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 80, 0, 255))
            elif max_el * 0.91 > zeors_array[x, y] >= max_el * 0.90:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 90, 0, 255))
            elif max_el * 0.90 > zeors_array[x, y] >= max_el * 0.89:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 100, 0, 255))
            elif max_el * 0.89 > zeors_array[x, y] >= max_el * 0.88:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 110, 0, 255))
            elif max_el * 0.88 > zeors_array[x, y] >= max_el * 0.87:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 120, 0, 255))
            elif max_el * 0.87 > zeors_array[x, y] >= max_el * 0.86:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 130, 0, 255))
            elif max_el * 0.86 > zeors_array[x, y] >= max_el * 0.85:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 140, 0, 255))
            elif max_el * 0.85 > zeors_array[x, y] >= max_el * 0.84:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 150, 0, 255))
            elif max_el * 0.84 > zeors_array[x, y] >= max_el * 0.83:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 160, 0, 255))
            elif max_el * 0.83 > zeors_array[x, y] >= max_el * 0.82:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 170, 0, 255))
            elif max_el * 0.82 > zeors_array[x, y] >= max_el * 0.81:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 180, 0, 255))
            elif max_el * 0.81 > zeors_array[x, y] >= max_el * 0.80:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 190, 0, 255))
            elif max_el * 0.80 > zeors_array[x, y] >= max_el * 0.79:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 200, 0, 255))
            elif max_el * 0.79 > zeors_array[x, y] >= max_el * 0.78:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 210, 0, 255))
            elif max_el * 0.78 > zeors_array[x, y] >= max_el * 0.77:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 220, 0, 255))
            elif max_el * 0.77 > zeors_array[x, y] >= max_el * 0.76:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 230, 0, 255))
            elif max_el * 0.76 > zeors_array[x, y] >= max_el * 0.75:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 240, 0, 255))
            elif max_el * 0.75 > zeors_array[x, y] >= max_el * 0.74:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 255, 0, 255))
            elif max_el * 0.74 > zeors_array[x, y] >= max_el * 0.73:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(240, 255, 0, 255))
            elif max_el * 0.73 > zeors_array[x, y] >= max_el * 0.72:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(230, 255, 0, 255))
            elif max_el * 0.72 > zeors_array[x, y] >= max_el * 0.71:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(220, 255, 0, 255))
            elif max_el * 0.71 > zeors_array[x, y] >= max_el * 0.70:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(210, 255, 0, 255))
            elif max_el * 0.70 > zeors_array[x, y] >= max_el * 0.69:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(200, 255, 0, 255))
            elif max_el * 0.69 > zeors_array[x, y] >= max_el * 0.68:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(190, 255, 0, 255))
            elif max_el * 0.68 > zeors_array[x, y] >= max_el * 0.67:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(180, 255, 0, 255))
            elif max_el * 0.67 > zeors_array[x, y] >= max_el * 0.66:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(170, 255, 0, 255))
            elif max_el * 0.66 > zeors_array[x, y] >= max_el * 0.65:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(160, 255, 0, 255))
            elif max_el * 0.65 > zeors_array[x, y] >= max_el * 0.64:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(150, 255, 0, 255))
            elif max_el * 0.64 > zeors_array[x, y] >= max_el * 0.63:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(140, 255, 0, 255))
            elif max_el * 0.63 > zeors_array[x, y] >= max_el * 0.62:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(130, 255, 0, 255))
            elif max_el * 0.62 > zeors_array[x, y] >= max_el * 0.61:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(120, 255, 0, 255))
            elif max_el * 0.61 > zeors_array[x, y] >= max_el * 0.60:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(110, 255, 0, 255))
            elif max_el * 0.60 > zeors_array[x, y] >= max_el * 0.59:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(100, 255, 0, 255))
            elif max_el * 0.59 > zeors_array[x, y] >= max_el * 0.58:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(90, 255, 0, 255))
            elif max_el * 0.58 > zeors_array[x, y] >= max_el * 0.57:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(80, 255, 0, 255))
            elif max_el * 0.57 > zeors_array[x, y] >= max_el * 0.56:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(70, 255, 0, 255))
            elif max_el * 0.56 > zeors_array[x, y] >= max_el * 0.55:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(60, 255, 0, 255))
            elif max_el * 0.55 > zeors_array[x, y] >= max_el * 0.54:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(50, 255, 0, 255))
            elif max_el * 0.54 > zeors_array[x, y] >= max_el * 0.53:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(40, 255, 0, 255))
            elif max_el * 0.53 > zeors_array[x, y] >= max_el * 0.52:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(30, 255, 0, 255))
            elif max_el * 0.52 > zeors_array[x, y] >= max_el * 0.51:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(20, 255, 0, 255))
            elif max_el * 0.51 > zeors_array[x, y] >= max_el * 0.50:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(10, 255, 0, 255))
            elif max_el * 0.50 > zeors_array[x, y] >= max_el * 0.49:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 255, 0, 255))
            elif max_el * 0.49 > zeors_array[x, y] >= max_el * 0.48:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 235, 255, 255))
            elif max_el * 0.48 > zeors_array[x, y] >= max_el * 0.47:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 235, 255, 255))
            elif max_el * 0.47 > zeors_array[x, y] >= max_el * 0.46:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 225, 255, 255))
            elif max_el * 0.46 > zeors_array[x, y] >= max_el * 0.45:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 215, 255, 255))
            elif max_el * 0.45 > zeors_array[x, y] >= max_el * 0.44:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 205, 255, 255))
            elif max_el * 0.44 > zeors_array[x, y] >= max_el * 0.43:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 195, 255, 255))
            elif max_el * 0.43 > zeors_array[x, y] >= max_el * 0.42:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 185, 255, 255))
            elif max_el * 0.42 > zeors_array[x, y] >= max_el * 0.41:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 175, 255, 255))
            elif max_el * 0.41 > zeors_array[x, y] >= max_el * 0.40:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 165, 255, 255))
            elif max_el * 0.40 > zeors_array[x, y] >= max_el * 0.39:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 155, 255, 255))
            elif max_el * 0.39 > zeors_array[x, y] >= max_el * 0.38:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 145, 255, 255))
            elif max_el * 0.38 > zeors_array[x, y] >= max_el * 0.37:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 135, 255, 255))
            elif max_el * 0.37 > zeors_array[x, y] >= max_el * 0.36:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 125, 255, 255))
            elif max_el * 0.36 > zeors_array[x, y] >= max_el * 0.35:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 115, 255, 255))
            elif max_el * 0.35 > zeors_array[x, y] >= max_el * 0.34:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 105, 255, 255))
            elif max_el * 0.34 > zeors_array[x, y] >= max_el * 0.33:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 95, 255, 255))
            elif max_el * 0.33 > zeors_array[x, y] >= max_el * 0.32:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 85, 255, 255))
            elif max_el * 0.32 > zeors_array[x, y] >= max_el * 0.31:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 75, 255, 255))
            elif max_el * 0.31 > zeors_array[x, y] >= max_el * 0.30:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 65, 255, 255))
            elif max_el * 0.30 > zeors_array[x, y] >= max_el * 0.29:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 55, 255, 255))
            elif max_el * 0.29 > zeors_array[x, y] >= max_el * 0.28:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 45, 255, 255))
            elif max_el * 0.28 > zeors_array[x, y] >= max_el * 0.27:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 35, 255, 255))
            elif max_el * 0.27 > zeors_array[x, y] >= max_el * 0.26:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 25, 255, 255))
            elif max_el * 0.26 > zeors_array[x, y] >= max_el * 0.25:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 25, 255, 255))
            elif max_el * 0.25 > zeors_array[x, y] >= max_el * 0.05:
                qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 0, 255, 255))
            # else:
            #     print(f'zer_arr{zeors_array[x,y]}')

    print('end draw')
    pixmap_zone = QtGui.QPixmap.fromImage(qimg_zone)
    # Положим одну картинку на другую
    painter = QtGui.QPainter(pixmap)
    painter.begin(pixmap)
    painter.setOpacity(self.opacity.value())
    painter.drawPixmap(0, 0, pixmap_zone)
    painter.end()
    # Разместим на сцене pixmap с pixmap_zone
    self.scene.addPixmap(pixmap)
    self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))