import face_recognition
import cv2
import os
import pickle

DATA_FILE = "students_data.pkl"

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        student_data = pickle.load(f)
else:
    student_data = {}

def register_student():
    cap = cv2.VideoCapture(0)
    print("📸 Show your face. Press 's' to save.")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                encoding = face_recognition.face_encodings(frame, face_locations)[0]

                # Get student details
                name = input("Enter Name: ")
                roll = input("Enter Roll Number: ")
                department = input("Enter Department: ")
                college = input("Enter College Name: ")

                student_data[name] = {
                    "encoding": encoding,
                    "roll": roll,
                    "department": department,
                    "college": college
                }

                with open(DATA_FILE, "wb") as f:
                    pickle.dump(student_data, f)

                print("✅ Registration successful!")
            else:
                print("❌ No face found. Try again.")
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_student():
    cap = cv2.VideoCapture(0)
    print("🧠 Recognizing... Press 'q' to quit.")

    known_encodings = [v["encoding"] for v in student_data.values()]
    known_names = list(student_data.keys())

    while True:
        ret, frame = cap.read()
        cv2.imshow("Recognize Face", frame)

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]
                student = student_data[name]

                print(f"\n✅ Match Found:")
                print(f"Name      : {name}")
                print(f"Roll No   : {student['roll']}")
                print(f"Department: {student['department']}")
                print(f"College   : {student['college']}\n")

                cap.release()
                cv2.destroyAllWindows()
                return

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main Menu
choice = input("Choose: [1] Register Student  [2] Recognize Student: ")
if choice == "1":
    register_student()
else:
    recognize_student()
