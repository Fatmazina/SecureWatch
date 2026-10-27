import cv2, os
import sys

def enroll_person(name, n_photos=20):
    save_dir = f'data/faces/{name}'
    os.makedirs(save_dir, exist_ok=True)
    cap = cv2.VideoCapture(0)
    count = 0
    print(f'Capturing {n_photos} photos for {name}. Press SPACE to capture.')
    while count < n_photos:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow('Enrollment', frame)
        key = cv2.waitKey(1)
        if key == ord(' '):
            cv2.imwrite(f'{save_dir}/{count:03d}.jpg', frame)
            count += 1
            print(f'  Captured {count}/{n_photos}')
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        person_name = sys.argv[1]
        enroll_person(person_name)
    else:
        print("Please provide a name for the person to enroll.")
        print("Usage: python enroll.py <person_name>")
