# Image Processing Utilities in Python

This repository provides a set of functions for performing basic image processing tasks in Python. These functions leverage libraries like `scikit-image` and `matplotlib`.

---

## Function Descriptions

### 1. Image Resizing:

- **`resize_image(image, proportion)`**:  
  This function resizes an image proportionally. It takes two arguments:
  - `image`: The input image as a NumPy array.
  - `proportion`: A float value between 0 and 1 representing the desired scaling factor.
  
  The function asserts that the provided proportion is valid and then calculates the new height and width based on the original image shape and the proportion. Finally, it uses `skimage.transform.resize` to resize the image with anti-aliasing for smoother scaling.

### 2. Image Plotting:

- **`plot_image(image)`**:  
  This function displays an image using `matplotlib`. It takes a single argument:
  - `image`: The image as a NumPy array.
  
  The function creates a figure, uses `imshow` to display the image in grayscale, turns off the axis labels, and shows the plot.

- **`plot_result(*args)`**:  
  This function plots multiple images in a row for comparison. It takes a variable number of arguments, each representing an image.
  
  The function creates a figure with a grid of subplots based on the number of images provided. It assigns titles to each image (including "Result" for the last one) and displays them using `imshow` with grayscale and disabled axis labels. Finally, it adjusts the layout and shows the plot.

- **`plot_histogram(image)`**:  
  This function visualizes the histogram of each color channel in an image. It takes a single argument:
  - `image`: The image as a NumPy array (assumed to be RGB).
  
  The function creates a figure with three subplots sharing the same x and y axes. It iterates through each color channel (red, green, blue), calculates the histogram, and plots it using `hist` with its corresponding color. Finally, it adjusts the layout and shows the plot.

### 3. Image Input/Output:

- **`read_image(path, is_gray=False)`**:  
  This function reads an image from a specified path. It takes two arguments:
  - `path`: The path to the image file.
  - `is_gray` (optional): A boolean flag indicating whether to read the image in grayscale. Defaults to `False` (color).
  
  The function uses `skimage.io.imread` to read the image and returns it as a NumPy array. If `is_gray` is `True`, the image is converted to grayscale before returning.

- **`save_image(image, path)`**:  
  This function saves an image to a specified path. It takes two arguments:
  - `image`: The image as a NumPy array.
  - `path`: The path where the image should be saved.
  
  The function uses `skimage.io.imsave` to save the image to the specified location.

### 4. Image Comparison:

- **`find_difference(image1, image2)`**:  
  This function calculates the structural similarity (SSIM) between two images and displays the difference image. It takes two arguments:
  - `image1`: The first image as a NumPy array.
  - `image2`: The second image as a NumPy array.
  
  The function asserts that both images have the same shape. It then converts them to grayscale and uses `skimage.metrics.structural_similarity` to calculate the SSIM score (a value between 0 and 1, where 1 indicates perfect similarity). It also retrieves the difference image. The function prints the SSIM score and returns the normalized difference image for further analysis.

- **`transfer_histogram(image1, image2)`**:  
  This function transfers the histogram of one image to another. It takes two arguments:
  - `image1`: The reference image as a NumPy array (from which the histogram will be transferred).
  - `image2`: The target image as a NumPy array (whose histogram will be adjusted).
  
  The function uses `skimage.exposure.match_histograms` to match the histograms of both images in all channels (assuming RGB), effectively transferring the color distribution from the reference image. The function returns the image with the adjusted histogram.

Feel free to use and adapt these functions for your image processing needs!

---

# Utilitários de Processamento de Imagens em Python

Este repositório fornece um conjunto de funções para realizar tarefas básicas de processamento de imagens em Python. Essas funções utilizam bibliotecas como `scikit-image` e `matplotlib`.

---

## Descrição das Funções

### 1. Redimensionamento de Imagem:

- **`resize_image(image, proportion)`**:  
  Esta função redimensiona uma imagem proporcionalmente. Ela aceita dois argumentos:
  - `image`: A imagem de entrada como um array NumPy.
  - `proportion`: Um valor float entre 0 e 1 representando o fator de escala desejado.
  
  A função garante que a proporção fornecida seja válida e, em seguida, calcula a nova altura e largura com base na forma da imagem original e na proporção. Por fim, utiliza `skimage.transform.resize` para redimensionar a imagem com antisserrilhamento para uma escala mais suave.

### 2. Exibição de Imagem:

- **`plot_image(image)`**:  
  Esta função exibe uma imagem usando o `matplotlib`. Ela aceita um único argumento:
  - `image`: A imagem como um array NumPy.
  
  A função cria uma figura, usa `imshow` para exibir a imagem em escala de cinza, desativa os rótulos dos eixos e mostra a imagem.

- **`plot_result(*args)`**:  
  Esta função exibe várias imagens em sequência para comparação. Ela aceita um número variável de argumentos, cada um representando uma imagem.
  
  A função cria uma figura com uma grade de subplots com base no número de imagens fornecidas. Ela atribui títulos a cada imagem (incluindo "Resultado" para a última) e as exibe usando `imshow` em escala de cinza, com rótulos de eixos desativados. Por fim, ajusta o layout e exibe o gráfico.

- **`plot_histogram(image)`**:  
  Esta função visualiza o histograma de cada canal de cor em uma imagem. Ela aceita um único argumento:
  - `image`: A imagem como um array NumPy (assumido ser RGB).
  
  A função cria uma figura com três subplots compartilhando os mesmos eixos x e y. Ela itera por cada canal de cor (vermelho, verde, azul), calcula o histograma e o exibe usando `hist` com sua cor correspondente. Finalmente, ajusta o layout e exibe o gráfico.

### 3. Entrada/Saída de Imagem:

- **`read_image(path, is_gray=False)`**:  
  Esta função lê uma imagem de um caminho especificado. Ela aceita dois argumentos:
  - `path`: O caminho para o arquivo de imagem.
  - `is_gray` (opcional): Um flag booleano indicando se a imagem deve ser lida em escala de cinza. O valor padrão é `False` (cor).
  
  A função usa `skimage.io.imread` para ler a imagem e retorná-la como um array NumPy. Se `is_gray` for `True`, a imagem é convertida para escala de cinza antes de ser retornada.

- **`save_image(image, path)`**:  
  Esta função salva uma imagem em um caminho especificado. Ela aceita dois argumentos:
  - `image`: A imagem como um array NumPy.
  - `path`: O caminho onde a imagem deve ser salva.
  
  A função usa `skimage.io.imsave` para salvar a imagem na localização especificada.

### 4. Comparação de Imagem:

- **`find_difference(image1, image2)`**:  
  Esta função calcula a similaridade estrutural (SSIM) entre duas imagens e exibe a imagem da diferença. Ela aceita dois argumentos:
  - `image1`: A primeira imagem como um array NumPy.
  - `image2`: A segunda imagem como um array NumPy.
  
  A função garante que ambas as imagens tenham o mesmo formato. Em seguida, as converte para escala de cinza e utiliza `skimage.metrics.structural_similarity` para calcular o índice de SSIM (um valor entre 0 e 1, onde 1 indica similaridade perfeita). Ela também obtém a imagem da diferença. A função imprime o índice SSIM e retorna a imagem da diferença normalizada para uma análise mais detalhada.

- **`transfer_histogram(image1, image2)`**:  
  Esta função transfere o histograma de uma imagem para outra. Ela aceita dois argumentos:
  - `image1`: A imagem de referência como um array NumPy (da qual o histograma será transferido).
  - `image2`: A imagem alvo como um array NumPy (cujo histograma será ajustado).
  
  A função usa `skimage.exposure.match_histograms` para ajustar os histogramas de ambas as imagens em todos os canais (assumindo RGB), transferindo efetivamente a distribuição de cores da imagem de referência. A função retorna a imagem com o histograma ajustado.

Sinta-se à vontade para usar e adaptar essas funções conforme suas necessidades de processamento de imagem!

---  