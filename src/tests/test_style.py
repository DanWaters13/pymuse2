from src.core.style import Style

def test_style(indent="", verbose=True):
    try:
        # Create a Style instance with default parameters
        style = Style()
        
        # Check if the font object is successfully created
        if style.font is not None:
            if verbose:
                print(f"{indent}Font loaded successfully.")
            return True
        else:
            if verbose:
                print(f"{indent}Font loading failed.")
            return False
    except Exception as e:
        if verbose:
            print(f"{indent}Error during test: {e}")
        return False