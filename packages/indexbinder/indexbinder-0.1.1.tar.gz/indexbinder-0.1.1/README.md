# IndexBinder

A very small library to help you store and retrieve faiss indexes from cloud storage

## Installation

You can install this library using pip:

```
pip install indexbinder
```

## Usage

Here's a basic example of how to use the image search functionality:

```python
from indexbinder import ImageSearch
from PIL import Image

# Create an ImageSearch instance
image_search = ImageSearch(
        "test_index", "google-project-name", "gcs-bucket", check_consistency=True
    )

image_search.add_image("path/to/your/image.jpg", {"example":  "metadata"})})


results = image_search.search(input_image, num_results=5)

# Process the results
for img, similarity in results:
    print(f"Similarity: {similarity}")
    img.show()  # Display the image
```

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment
3. Install the development dependencies:
   ```
   pip install -e ".[dev]"
   ```

## Testing

To run the tests:

```
pytest
```
