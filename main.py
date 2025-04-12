import datetime
import re
from typing import Dict, Union
import streamlit as st
# from dateparser import parse  # Import dateparser  <-- Removed this line

def convert_natural_language_to_code(text: str) -> Dict[str, Union[str, None]]:
    """
    Converts natural language describing a date/time into code snippets.

    Args:
        text: The natural language text to convert (e.g., "next Tuesday at 3 PM").

    Returns:
        A dictionary containing code snippets in different languages,
        or None if the input cannot be parsed.
    """
    # parsed_datetime = parse(text)  # Use dateparser <-- Removed dateparser
    #  Use datetime.datetime.strptime() and handle more natural language
    try:
        # Attempt to parse the text.  This will raise a ValueError if it fails.
        #  We'll try a few common formats.
        parsed_datetime = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")  # Example: 2024-08-15 14:30:00
    except ValueError:
        try:
            parsed_datetime = datetime.datetime.strptime(text, "%Y-%m-%d") # Example 2024-08-15
        except ValueError:
            try:
               parsed_datetime = datetime.datetime.strptime(text, "%d/%m/%Y")
            except ValueError:
                try:
                    parsed_datetime = datetime.datetime.strptime(text, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    return {
                        "error": "Sorry, I couldn't understand that date/time.  Please use a format like %Y-%m-%d %H:%M:%S, %Y-%m-%d, %d/%m/%Y, or %d/%m/%Y %H:%M:%S"
                    }

    if parsed_datetime is None:
        return {
            "error": "Sorry, I couldn't understand that date/time."
        }

    try:
        # Python datetime object
        python_code = f"datetime.datetime({parsed_datetime.year}, {parsed_datetime.month}, {parsed_datetime.day}, {parsed_datetime.hour}, {parsed_datetime.minute})"

        # JavaScript Date object
        javascript_code = f"new Date('{parsed_datetime.isoformat()}')"

        # Java Date object
        java_code = f"new SimpleDateFormat(\"yyyy-MM-dd HH:mm:ss\").parse(\"{parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')}\")"

        # C# DateTime object
        csharp_code = f"DateTime.Parse(\"{parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')}\")"

        # PHP DateTime object
        php_code = f"DateTime::createFromFormat('Y-m-d H:i:s', '{parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')}')"

        return {
            "natural_language": text,
            "python": python_code,
            "javascript": javascript_code,
            "java": java_code,
            "csharp": csharp_code,
            "php": php_code,
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}



def main():
    """
    Main function to run the Streamlit application.
    """
    # Set the title of the app
    st.title("Natural Language to Code Converter")

    # Apply a gradient background using CSS
    st.markdown(
        """
        <style>
        .reportview-container {
            /* Removed background to fix the issue */
            color: white; /* Default text color */
        }
        .main h1, .main p, .main label, .main div, .main span, .main code {
            color: #000000 !important; /* Make all text black */
        }
        .stTextInput>div>div>input {
            background-color: #ffffff;  /* Input background white */
            color: #000000;          /* Input text black */
        }
        .stButton>button {
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .streamlit-expander {
             background-color: #ffffff1a;
             border-radius: 8px;
             margin-bottom: 10px;
        }
        .streamlit-expander-header{
            color: #000000;
        }

        .streamlit-expander-content {
            color: #000000;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a description
    st.write("Enter a date and time in natural language (e.g., '2024-08-15 14:30:00').")

    # Create a text input field
    text = st.text_input("Enter date/time text:", key="text_input") # Add a key

    # Create a convert button
    if st.button("Convert", key="convert_button"): # Add a key
        if text:
            result = convert_natural_language_to_code(text)
            if "error" in result:
                st.error(result["error"])
            else:
                st.subheader("Code Snippets:")
                st.markdown(f"**Natural Language:** {result['natural_language']}", unsafe_allow_html=True)
                st.markdown(f"**Python:** <code style='background-color: #e0f7fa; color: #000000;'>{result['python']}</code>", unsafe_allow_html=True)
                st.markdown(f"**JavaScript:** <code style='background-color: #e0f7fa; color: #000000;'>{result['javascript']}</code>", unsafe_allow_html=True)
                st.markdown(f"**Java:** <code style='background-color: #e0f7fa; color: #000000;'>{result['java']}</code>", unsafe_allow_html=True)
                st.markdown(f"**C#:** <code style='background-color: #e0f7fa; color: #000000;'>{result['csharp']}</code>", unsafe_allow_html=True)
                st.markdown(f"**PHP:** <code style='background-color: #e0f7fa; color: #000000;'>{result['php']}</code>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a date/time string.")



if __name__ == "__main__":
    main()
