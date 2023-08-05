import pygame


def get_directories(anim_name):
    with open(f"assets/animations/{anim_name}/info.txt") as file:
        images_number = int(file.read().strip("\n"))
        coo = int(file.read().strip("\n"))
    return images_number, coo


def play_animation(screen: pygame.surface, anim_name, speed=1):
    image_numbers, coo = get_directories(anim_name)
    for image_dir in range(image_numbers):
        image = pygame.image.load(f"assets/Animations/{image_dir}.png")
        screen.blit(image, coo)
        pygame.display.update()
        pygame.time.wait(500*speed)
