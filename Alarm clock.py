import datetime
import time
try:
    import winsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("Sound playing functionality is not available on this system.")

class AlarmClock:
    def __init__(self):
        self.alarms = []
        self.running = True

    def set_alarm(self, time_str, tone, snooze_time):
        alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
        self.alarms.append({'time': alarm_time, 'tone': tone, 'snooze_time': snooze_time, 'active': True})
        print(f"Alarm set for {time_str} with tone '{tone}' and snooze time of {snooze_time} minutes.")

    def delete_alarm(self, time_str):
        alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
        self.alarms = [alarm for alarm in self.alarms if alarm['time'] != alarm_time]
        print(f"Alarm for {time_str} deleted.")

    def show_alarms(self):
        print("Current Alarms:")
        for alarm in self.alarms:
            status = "Active" if alarm['active'] else "Inactive"
            print(f"Time: {alarm['time']}, Tone: {alarm['tone']}, Snooze: {alarm['snooze_time']} mins, Status: {status}")

    def snooze_alarm(self, alarm):
        snooze_until = (datetime.datetime.combine(datetime.date.today(), alarm['time']) + 
                        datetime.timedelta(minutes=alarm['snooze_time'])).time()
        print(f"Snoozing alarm for {alarm['snooze_time']} minutes.")
        alarm['time'] = snooze_until
        alarm['active'] = True

    def play_tone(self, tone):
        if SOUND_ENABLED:
            try:
                winsound.PlaySound(tone, winsound.SND_FILENAME)
            except Exception as e:
                print(f"Error playing tone: {e}")
        else:
            print(f"Alarm tone would play here: {tone}")

    def check_alarms(self):
        while self.running:
            now = datetime.datetime.now().time()
            for alarm in self.alarms:
                if alarm['time'] <= now and alarm['active']:
                    print(f"Alarm ringing! Time: {alarm['time']}")
                    self.play_tone(alarm['tone'])
                    alarm['active'] = False
                    snooze = input("Snooze? (yes/no): ").strip().lower()
                    if snooze == 'yes':
                        self.snooze_alarm(alarm)
            time.sleep(1)

    def run(self):
        while True:
            print("\nOptions:")
            print("1. Set Alarm")
            print("2. Delete Alarm")
            print("3. Show Alarms")
            print("4. Exit")
            choice = input("Choose an option: ").strip()

            if choice == '1':
                time_str = input("Enter time (HH:MM): ").strip()
                tone = input("Enter alarm tone file path (must be .wav file): ").strip()
                snooze_time = int(input("Enter snooze time in minutes: ").strip())
                self.set_alarm(time_str, tone, snooze_time)
            elif choice == '2':
                time_str = input("Enter time of alarm to delete (HH:MM): ").strip()
                self.delete_alarm(time_str)
            elif choice == '3':
                self.show_alarms()
            elif choice == '4':
                self.running = False
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    alarm_clock = AlarmClock()
    alarm_clock.run()
    alarm_clock.check_alarms()
