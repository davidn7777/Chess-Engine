import streamlit as st
import ChessGame

def load_svg(svg_path):
    """Read SVG content from a file."""
    with open(svg_path, "r") as file:
        return file.read()


def main():
    col1,col2 = st.columns(2)
    with col1:
        with st.container():
            if 'fen' not in st.session_state:
                st.session_state.fen = ChessGame.gen_board()  # Initial value      
            
            # Set the title of the app
            st.title('Chat Chess')
            
            # User input for UCI move
            uci_move = st.text_input('Enter your UCI move')


    with col2:
        with st.container():
            # Button to submit move
            if st.button('Submit Move'):
                st.write(f'You entered the move: {uci_move}')
                if uci_move in ChessGame.get_legal(st.session_state.fen):
                    st.session_state.fen = ChessGame.move(st.session_state.fen,uci_move)
                else:
                    st.error("Please input a legal move in the form: e2e4")

                svg_file = 'board.svg'  # Update the path to your SVG file
                svg_data = load_svg(svg_file)
                st.markdown(f'<div style="text-align: left;">{svg_data}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()

