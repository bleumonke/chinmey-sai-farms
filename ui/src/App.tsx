import React from "react";
import { Box, CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Layouts from "./pages/Layouts";
import CustomersTable from "./pages/tables/CustomersTable";
import Settings from "./pages/Settings";
import theme from "./theme";

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: "flex" }}>
        <Sidebar />
        <Box component="main" sx={{ flexGrow: 1, p: 3}}>
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/layouts" element={<Layouts />} />
            <Route path="/customers" element={<CustomersTable />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;
