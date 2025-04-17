import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    background: {
      default: "white",
      paper: "#3D3D3D",
    },
    primary: {
      main: "#1976d2",
    },
    text: {
      primary: "#ffffff",
      secondary: "#aaa",
    },
  },
  typography: {
    fontFamily: `"Roboto", "Helvetica", "Arial", sans-serif`,
    fontSize: 14,
  },
  components: {
    MuiListItemIcon: {
      styleOverrides: {
        root: {
          minWidth: 30,
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          gap: 8,
        },
      },
    },
  },
});

export default theme;
