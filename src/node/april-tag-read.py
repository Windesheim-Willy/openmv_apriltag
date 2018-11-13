 def spinonce(self):
        """Spin to read."""
        lines = []
        received = False

        while self.serial.in_waiting:
            line = self.serial.readline()
            lines.append(line)
            received = True

        codes = []
        if received:
            for line in lines:
                code = self.parseline(line)
                if code is not None:
                    codes.append(code)

            self.msg.header.stamp = (rospy.Time.now() - self.delay)
            self.msg.barcodes = codes
            self.barcode_to_world(self.msg)
            self.topic.publish(self.msg)