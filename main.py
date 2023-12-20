import itertools
import math
import random
import pygame
import glm

pygame.init()

comparison_resolution = glm.vec2(32, 32)
render_resolution = glm.vec2(comparison_resolution.x * 2, comparison_resolution.y)
window_size = render_resolution * 4


def mutate_gene_order(genes, mutation_rate, gene_size):
    gene_indices = list(range(len(genes)))
    num_genes = len(genes) // gene_size  # Assuming each gene has a fixed size

    for i in range(num_genes):
        if random.random() < mutation_rate:
            swap_index = random.randint(0, num_genes - 1)
            # Swap the positions of the genes in the list
            gene_indices[i], gene_indices[swap_index] = (
                gene_indices[swap_index],
                gene_indices[i],
            )

    # Reorder the genes based on the new indices
    mutated_genes = []
    for idx in gene_indices:
        gene_start = idx * gene_size
        mutated_genes.extend(genes[gene_start : gene_start + gene_size])

    return mutated_genes


def main():
    window = pygame.display.set_mode(
        window_size.to_tuple(),
        # make sure has alpha channel
        pygame.HWSURFACE,
    )
    pygame.display.set_caption("Triproxim8")

    render_surface = pygame.Surface(render_resolution.to_tuple(), pygame.HWSURFACE)
    page_surface = pygame.Surface(comparison_resolution.to_tuple(), pygame.HWSURFACE)

    im_path = "assets/fish.jpg"
    image = pygame.image.load(im_path)
    target_image = pygame.transform.scale(image, comparison_resolution.to_tuple())

    # initialize genes and search params
    mutation_rate = 0.001
    best_loss = float("inf")
    worse_count = 0
    genes = []
    num_genes = 256
    gene_size = 9
    for _ in range(0, num_genes):
        x1 = random.random()
        y1 = random.random()
        x2 = random.random()
        y2 = random.random()
        x3 = random.random()
        y3 = random.random()
        r = random.random()
        g = random.random()
        b = random.random()
        genes.extend([x1, y1, x2, y2, x3, y3, r, g, b])
    best_genes = genes.copy()

    # begin search
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False
        # change mutation rate
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            mutation_rate *= 1.01
        elif keys[pygame.K_DOWN]:
            mutation_rate /= 1.01

        render_surface.fill((0, 0, 0))
        page_surface.fill((0, 0, 0))

        # render the target image to the left
        render_surface.blit(target_image, (0, 0))

        # render genes
        for i in range(0, len(genes), gene_size):
            gene_chunk = genes[i : i + gene_size]
            x, y, x2, y2, x3, y3, r, g, b = gene_chunk
            pygame.draw.polygon(
                page_surface,
                (r * 255, g * 255, b * 255),
                (
                    (x * comparison_resolution.x, y * comparison_resolution.y),
                    (x2 * comparison_resolution.x, y2 * comparison_resolution.y),
                    (x3 * comparison_resolution.x, y3 * comparison_resolution.y),
                ),
                0,  # default: fills the polygon
            )
        render_surface.blit(
            page_surface,
            (comparison_resolution.x, 0),
            # special_flags=pygame.BLEND_RGBA_ADD,
        )

        stretched_surface = pygame.transform.scale(render_surface, window_size)
        window.blit(stretched_surface, (0, 0))
        # render mutation rate in top left
        font = pygame.font.SysFont("Arial", 16)
        dark_text = True
        text = font.render(
            f"Mutation rate: {mutation_rate}",
            True,
            (255, 255, 255) if not dark_text else (0, 0, 0),
        )
        window.blit(text, (0, 0))
        pygame.display.update()

        # compare rendered image to target image (at reduced resolution)
        loss = 0
        for x in range(int(comparison_resolution.x)):
            for y in range(int(comparison_resolution.y)):
                page_color = page_surface.get_at((x, y))
                target_color = target_image.get_at((x, y))
                loss += sum(abs(pc - tc) for pc, tc in zip(page_color, target_color))

        if loss < best_loss:
            best_loss = loss
            best_genes = genes.copy()
        else:
            genes = best_genes.copy()
        #     worse_count = 0
        # else:
        #     worse_count += 1
        #     if worse_count >= 20:
        #         mutation_rate /= 2
        #         worse_count = 0

        # mutate genes
        for i in range(len(genes)):
            gene = genes[i]
            mutation_chance = random.random()
            if mutation_chance < mutation_rate:
                delta = (random.random() * 2.0 - 1.0) * 0.1
                genes[i] = min(1, max(0, gene + delta))

                if mutation_chance < (mutation_rate * 0.5):  # critical mutation
                    genes[i] = random.random()
        genes = mutate_gene_order(genes, mutation_rate, gene_size)

    pygame.quit()


if __name__ == "__main__":
    main()
