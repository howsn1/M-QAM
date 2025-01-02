import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_qam_constellation():
    while True:
      
            M = int(input("Entrez le symbole M pour la constellation QAM (doit être ≥ 4 et une puissance de 2) : "))
            
            if M < 4 or math.log2(M) != int(math.log2(M)):
                print("Erreur : M doit être une puissance de 2 et ≥ 4.")
                continue

            m = int(math.log2(M))

            if m % 2 == 0:
                k = 2 ** (m // 2)
            else:
                k = 3 * (2 ** ((m - 3) // 2))

            weight = (k**2 - M) // 4
            side_len_remove = int(math.sqrt(weight)) 

        
            print("\n--- Détails de la Constellation QAM ---")
            print(f"Symbole M : {M}")
            print(f"Valeur de m : {m}")
            print(f"Valeur de k : {k}")
            print(f"Points à rejeter : {4*weight}")


            x = []
            y = []
            symbols = [] 
            offset = 0.5  
            for i in range(k):
                for j in range(k):
                    x.append(i - (k // 2) + offset)
                    y.append(j - (k // 2) + offset)
                    symbols.append(f"S({i},{j})")  
            
            x = np.array(x)
            y = np.array(y)
            symbols = np.array(symbols)

 
            removed_x = []
            removed_y = []
            indices_to_remove = []
            for i in range(side_len_remove):
                for j in range(side_len_remove):
                    # Toleft corner
                    indices_to_remove.append(i * k + j)
                    removed_x.append(i - (k // 2) + offset)
                    removed_y.append(j - (k // 2) + offset)
                    # TopRrigt corner
                    indices_to_remove.append(i * k + (k - 1 - j))
                    removed_x.append(i - (k // 2) + offset)
                    removed_y.append((k - 1 - j) - (k // 2) + offset)
                    # Bottom-Left corner
                    indices_to_remove.append((k - 1 - i) * k + j)
                    removed_x.append((k - 1 - i) - (k // 2) + offset)
                    removed_y.append(j - (k // 2) + offset)
                    # BottomRight corner
                    indices_to_remove.append((k - 1 - i) * k + (k - 1 - j))
                    removed_x.append((k - 1 - i) - (k // 2) + offset)
                    removed_y.append((k - 1 - j) - (k // 2) + offset)

            # Remove  points
            x = np.delete(x, indices_to_remove)
            y = np.delete(y, indices_to_remove)
            symbols = np.delete(symbols, indices_to_remove)

            # Plot original constellation
            plt.figure(figsize=(8, 8))
            plt.scatter(x, y, c='blue', s=20, label="Constellation Points")
            plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
            plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')
            plt.title(f"Constellation M-QAM (Originale) pour M = {M}")
            plt.xlabel("In-Phase")
            plt.ylabel("Quadrature")
            plt.legend()
            plt.grid(True)
            plt.show()

            # Select points for analysis
            print("\n--- Choix des points de déclenchement ---")
            for idx, symbol in enumerate(symbols):
                print(f"{idx}: {symbol} -> ({x[idx]:.2f}, {y[idx]:.2f})")
            selected_indices = input("Entrez les indices des points à analyser, séparés par des virgules : ")
            selected_indices = [int(i.strip()) for i in selected_indices.split(',') if i.strip().isdigit()]
            if not selected_indices or any(idx < 0 or idx >= len(x) for idx in selected_indices):
                print("Indices invalides. Aucun calcul effectué pour ces points.")
                continue

            # Calculate energy and phase for selected points
            print("\n--- Bilan Energétique et Phase ---")
            for idx in selected_indices:
                energy = x[idx]*2 + y[idx]*2
                phase = np.arctan2(y[idx], x[idx])
                print(f"Point {symbols[idx]} : Energie = {energy:.2f}, Phase = {phase:.2f} radians")

            # Add Noise
            noise_type = input("\nType de bruit à ajouter (gaussian/uniform) : ").strip().lower()
            if noise_type not in ["gaussian", "uniform"]:
                print("Type de bruit non valide. Veuillez entrer 'gaussian' ou 'uniform'.")
                continue  # Recommencer la boucle
            noise_level = float(input("Niveau de bruit (sigma pour Gaussian, range pour Uniform) : "))
            if noise_type == "gaussian":
                noise_x = np.random.normal(0, noise_level, len(x))
                noise_y = np.random.normal(0, noise_level, len(y))
            elif noise_type == "uniform":
                noise_x = np.random.uniform(-noise_level, noise_level, len(x))
                noise_y = np.random.uniform(-noise_level, noise_level, len(y))

            # Apply noise to the points
            x_noisy = x + noise_x
            y_noisy = y + noise_y

            # Plot constellation with noise only
            plt.figure(figsize=(8, 8))
            plt.scatter(x_noisy, y_noisy, c='red', s=20, label="Noisy Points")
            plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
            plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')
            plt.title(f"Constellation M-QAM avec Bruit (Seulement) pour M = {M}")
            plt.xlabel("In-Phase")
            plt.ylabel("Quadrature")
            plt.legend()
            plt.grid(True)
            plt.show()

            # Ask if user wants to continue
            continue_calc = input("\nVoulez-vous calculer une autre constellation ? (Y/N) : ")
            if not continue_calc.lower().startswith('N'):
                break

      

if __name__ == "__main__":
    calculate_qam_constellation()
    print("Merci d'avoir utilisé le Calculateur de Constellation QAM !")