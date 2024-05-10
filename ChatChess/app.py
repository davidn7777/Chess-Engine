import streamlit as st
import ChessGame

def load_svg(svg_path):
    """Read SVG content from a file."""
    with open(svg_path, "r") as file:
        return file.read()

def app():
    col1,col2 = st.columns(2)

    if 'fen' not in st.session_state:
        st.session_state.fen = ChessGame.gen_board()  

    if 'svg_data' not in st.session_state:
        svg_file = 'board.svg'
        st.session_state.svg_data = load_svg(svg_file)

    with col1:
        with st.container():  
            st.title('Chat Chess')
            uci_move = st.text_input('Enter your UCI move')


    with col2:
        with st.container():
            if 'runtime' not in st.session_state:
                st.session_state.runtime = True
                svg_file = 'board.svg'
                st.session_state.svg_data = load_svg(svg_file)

            if st.button('Submit Move'):
                st.write(f'You entered the move: {uci_move}')
                if uci_move in ChessGame.get_legal(st.session_state.fen):
                    st.session_state.fen = ChessGame.move(st.session_state.fen,uci_move)
                    svg_file = 'board.svg'
                    st.session_state.svg_data = load_svg(svg_file)
                else:
                    st.error("Please input a legal move in the form: e2e4")

            st.markdown(f'<div style="text-align: left;">{st.session_state.svg_data}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    app()

