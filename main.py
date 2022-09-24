import os
import pyautogui
import numpy as np
import threading

FULLSCREEN = X, Y, WIDTH, HEIGHT = 0, 0, 1920, 1080
PLAYER_CENTER: tuple = 960, 520
PLAYER_AREA: tuple = 885, 460, 150, 120

ROOT = os.path.dirname(__file__)
COORD = os.path.join(ROOT, "coord")
REFRESHING_AREA = os.path.join(ROOT, "refreshing_area")
UNLOCK_FOR_PICKING_LOOT = os.path.join(ROOT, "unlock_for_picking_loot")
IMAGES_ROOT = os.path.join(ROOT, 'images')

ANGLE_SOLUTIONS = {
    # in range 900 - 1019 of x and 519 - 0 of y angle
    "up_angle": (900, 1019, 519, 0),
    "up_right_angle": (1020, 1920, 400, 0),
    "right_angle": (1019, 1920, 401, 500),
    "right_down_angle": (1020, 1920, 520, 1080),
    "down_angle": (900, 1019, 520, 1080),
    "left_down_angle": (0, 1020, 520, 1080),
    "left_angle": (0, 1019, 401, 500),
    "left_up_angle": (0, 1920, 400, 0),
}
SOLUTIONS = {
    "unlock_for_picking_loot": {
        os.path.join(IMAGES_ROOT, 'aberrant_corroded.png'): PLAYER_AREA,
        os.path.join(IMAGES_ROOT, 'azurite.png'): PLAYER_AREA,
        os.path.join(IMAGES_ROOT, 'currency.png'): PLAYER_AREA,
        os.path.join(IMAGES_ROOT, 'perfect.png'): PLAYER_AREA,
        os.path.join(IMAGES_ROOT, 'dense.png'): PLAYER_AREA
    },

    "refreshing_area": {
        os.path.join(IMAGES_ROOT, 'ending_dot.png'): PLAYER_AREA,
        os.path.join(IMAGES_ROOT, 'ending_label.png'): FULLSCREEN,
        os.path.join(IMAGES_ROOT, 'load_screen.png'): FULLSCREEN,
        os.path.join(IMAGES_ROOT, 'subterrain.png'): FULLSCREEN
    }
}


def show():

    cv2 = None

    while True:
        image = pyautogui.screenshot(region=PLAYER_AREA)
        image_array = np.array(image)
        frame = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

        cv2.imshow("test", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()


# Think this is bad decision but i don't remember why this implement like this
# And actually pyautogui is slow so, for better performance should use win32 api for creating bitmap and then parsing it
unlock_for_picking_loot = 0
refreshing_area = 0
coord = ()
unlock_for_picking_loot_count = len(os.listdir(UNLOCK_FOR_PICKING_LOOT))
refreshing_area_count = len(os.listdir(REFRESHING_AREA))
coord_count = len(os.listdir(COORD))

unlock_for_picking_loot_image = ()
refreshing_area_image = ()
coord_image = ()


def main() -> None:
    global unlock_for_picking_loot
    global refreshing_area
    global coord
    global unlock_for_picking_loot_image
    global refreshing_area_image
    global coord_image

    while True:

        pos_x, pos_y = pyautogui.position()

        def unlock() -> None:
            global unlock_for_picking_loot
            global unlock_for_picking_loot_count
            global unlock_for_picking_loot_image

            for img, coord in SOLUTIONS["unlock_for_picking_loot"].items():
                if pyautogui.locateOnScreen(img, confidence=0.65, region=coord):
                    unlock_for_picking_loot = "unlock_for_picking_loot"

                    path = os.path.join(
                        ROOT,
                        *[
                            "unlock_for_picking_loot",
                            f'unlock_for_picking_loot-{unlock_for_picking_loot_count}.png'
                        ]
                    )

                    unlock_for_picking_loot_count += 1
                    unlock_for_picking_loot_image = pyautogui.screenshot(), path

                    return None
            unlock_for_picking_loot = 1

        def refreshing() -> None:
            global refreshing_area
            global refreshing_area_count
            global refreshing_area_image

            for img, coord in SOLUTIONS["refreshing_area"].items():
                if pyautogui.locateOnScreen(img, confidence=0.65, region=coord):
                    refreshing_area = "refreshing_area"

                    path = os.path.join(
                        ROOT,
                        *[
                            "refreshing_area",
                            f'refreshing_area-{refreshing_area_count}.png'
                        ]
                    )
                    refreshing_area_count += 1
                    pyautogui.screenshot(path)

                    return None
            refreshing_area = 1

        def angle() -> None:
            global coord
            global coord_count
            global coord_image

            for solution, value in ANGLE_SOLUTIONS.items():
                if value[0] <= pos_x <= value[1] and value[2] <= pos_y <= value[3]:
                    coord = solution

                    path = os.path.join(
                        ROOT,
                        *[
                            "coord",
                            f'{solution}-{coord_count}.png'
                        ]
                    )

                    coord_count += 1
                    coord_image = pyautogui.screenshot(), path
                    return None

                elif value[0] <= pos_x <= value[1] and value[2] >= pos_y >= value[3]:
                    coord = solution

                    path = os.path.join(
                        ROOT,
                        *[
                            "coord",
                            f'{solution}-{coord_count}.png'
                        ]
                    )

                    coord_count += 1
                    coord_image = pyautogui.screenshot(), path
                    return None

        first = threading.Thread(target=unlock)
        second = threading.Thread(target=refreshing)
        third = threading.Thread(target=angle)

        first.start()
        second.start()
        third.start()

        first.join()
        second.join()
        third.join()

        while True:
            if unlock_for_picking_loot == 1 and refreshing_area == 1 and coord:
                print(coord)
                coord_image[0].save(coord_image[1])
                break

            elif unlock_for_picking_loot == "unlock_for_picking_loot":
                print(unlock_for_picking_loot)
                refreshing_area_image[0].save(refreshing_area_image[1])
                break

            elif refreshing_area == "refreshing_area":
                print(refreshing_area)
                refreshing_area_image[0].save(refreshing_area_image[1])
                break

        unlock_for_picking_loot = 0
        refreshing_area = 0
        coord = ()

        unlock_for_picking_loot_image = ()
        refreshing_area_image = ()
        coord_image = ()


# threading.Thread(target=show, name="show").start()
threading.Thread(target=main, name="main").start()
