"""Pygame display for the Arduino ultrasonic sensor project."""
import argparse
import os
import sys

import pygame
import serial
from serial.tools import list_ports


def available_ports():
    ports = [p.device for p in list_ports.comports()]
    return ", ".join(ports) if ports else "No serial ports detected"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--port",
        default=os.environ.get("ARDUINO_PORT", "COM5"),
        help="Arduino serial port (default: ARDUINO_PORT env var or COM5)",
    )
    parser.add_argument("--baud", type=int, default=9600, help="Serial baud rate")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        connection = serial.Serial(args.port, args.baud, timeout=1)
    except serial.SerialException as exc:
        print(f"Could not open serial port {args.port}: {exc}", file=sys.stderr)
        print(f"Available ports: {available_ports()}", file=sys.stderr)
        print("Close Arduino Serial Monitor/Plotter and try again.", file=sys.stderr)
        return 1

    # Many Arduino boards reset when the serial port opens.
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Arduino Ultrasonic Sensor")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 24)

    image_path = os.path.join(os.path.dirname(__file__), "assets", "car1.png")
    try:
        background_image = pygame.image.load(image_path).convert()
        background_image = pygame.transform.scale(background_image, (500, 500))
    except (pygame.error, FileNotFoundError):
        background_image = None

    distance_text = "Waiting for Arduino..."
    buffer = b""
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Read one line only; avoid consuming two readings per screen frame.
            try:
                if connection.in_waiting:
                    line = connection.readline().decode("ascii", errors="ignore").strip()
                    if line:
                        try:
                            cm = int(line)
                            distance_text = "No echo detected" if cm < 0 else f"Distance: {cm} cm"
                        except ValueError:
                            distance_text = f"Invalid serial data: {line[:30]}"
            except serial.SerialException as exc:
                distance_text = f"Serial error: {exc}"

            if background_image is not None:
                screen.blit(background_image, (0, 0))
                # Semi-opaque background is avoided for broad pygame compatibility.
                pygame.draw.rect(screen, (30, 30, 30), (0, 12, 500, 48))
                text_color = (255, 255, 0)
            else:
                screen.fill((205, 129, 98))
                text_color = (255, 255, 0)

            label = font.render(distance_text, True, text_color)
            screen.blit(label, (12, 20))
            pygame.display.flip()
            clock.tick(30)
    finally:
        connection.close()
        pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
