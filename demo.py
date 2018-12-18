import cv2
import numpy as np
 
cap = cv2.VideoCapture('test.mp4')
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (960,720))

 
# Create old frame
_, frame = cap.read()
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
# Lucas kanade params
lk_params = dict(winSize = (20, 20),
                 maxLevel = 4,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
 
old_points_list = []
points_list = []
# Mouse function
def select_point(event, x, y, flags, params):
    global point, point_selected, old_points, old_points_list, points_list
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        points_list.append(point)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)
        old_points_list.append(old_points)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)

# horiozontal_direction = ['Left', 'Right', 'straight']

point_selected = False
point = ()
old_points = np.array([[]])
while True:
    ret, frame = cap.read()
    print('---------------',ret)
    if ret == False:
        break
    print('BREAKED')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    horiozontal_direction = ''
    left_count = 0
    straight_count = 0
    right_count = 0
    # print('old_points_list', old_points_list)
    # print('points_list', points_list)
    print(type(old_points_list))
    print(old_points_list)
    old_points_list_copy = old_points_list.copy()
    points_list_copy = points_list.copy()
    old_points_list = []
    points_list = []

    for i, points in enumerate(old_points_list_copy):
        x,y = points[0].ravel()
        points_x, points_y = points[0]
        print(x,y)
        if x<=0 or y<=0 or x>=960 or y>=720:
            continue
        else:
            old_points_list.append(points)
            points_list.append((points_x, points_y))
    # print(old_points_list)  
    # old_points_list = temp
    # old_points_list[old_points_list != 0]

    if point_selected is True:
        print('\n \n')
        for i, _ in enumerate(old_points_list):
            cv2.circle(frame, points_list[i], 5, (0, 0, 255), 2)
     
            new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points_list[i], None, **lk_params)
            print('distance', old_points[0][0]-new_points[0][0])
            old_points_list[i] = new_points
            if old_points[0][0]-new_points[0][0] > 35 and old_points[0][0]-new_points[0][0] > 0:
                horiozontal_direction = 'right'
                left_count += 1
            elif old_points[0][0]-new_points[0][0] < -35 and old_points[0][0]-new_points[0][0] < 0:
                horiozontal_direction = 'left'
                right_count += 1
            else:
                horiozontal_direction = 'straight'
                straight_count += 1

            x, y = new_points.ravel()
            font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(frame, horiozontal_direction, (50, 50), font, 1, (0, 255, 0), 1)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        old_gray = gray_frame.copy()
    print([left_count, right_count, straight_count])
    index = [left_count, right_count, straight_count].index(max([left_count, right_count, straight_count]))
    if index == 0:
        horiozontal_direction = 'Right'
    if index == 1:
        horiozontal_direction = 'Left'
    if index == 2:
        horiozontal_direction = 'straight'

    index = [straight_count, right_count, left_count].index(max([straight_count, right_count, left_count]))
    if index == 0:
        horiozontal_direction = 'straight'
    if index == 1:
        horiozontal_direction = 'Left'
    if index == 2:
        horiozontal_direction = 'Right'
    print('index',horiozontal_direction)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, horiozontal_direction, (100, 50), font, 1, (0, 0, 255), 1)
    cv2.imshow("Frame", frame)
 
    key = cv2.waitKey(0)
    if key == 27:
        break
    out.write(frame)

cap.release()
cv2.destroyAllWindows()
