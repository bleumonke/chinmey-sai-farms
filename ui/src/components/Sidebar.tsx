import React from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Box,
  useTheme,
} from "@mui/material";
import SpaceDashboardRoundedIcon from "@mui/icons-material/SpaceDashboardRounded";
import PhotoSizeSelectActualIcon from "@mui/icons-material/PhotoSizeSelectActual";
import SettingsIcon from '@mui/icons-material/Settings';
import GroupIcon from "@mui/icons-material/Group";
import { useNavigate, useLocation } from "react-router-dom";

const drawerWidth = 220;

const Sidebar: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { text: "Dashboard", path: "/dashboard", icon: <SpaceDashboardRoundedIcon /> },
    { text: "Layouts", path: "/layouts", icon: <PhotoSizeSelectActualIcon /> },
    { text: "Customers", path: "/customers", icon: <GroupIcon /> },
    { text: "Settings", path: "/settings", icon: <SettingsIcon /> },
  ];

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: "border-box",
          backgroundColor: theme.palette.background.paper,
          color: theme.palette.text.primary,
        },
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: theme.palette.background.paper,
          color: theme.palette.text.primary,
          height: 64,
          marginBottom: 10
        }}
      >
        <Typography variant="h6" noWrap component="div">
          MyApp
        </Typography>
      </Toolbar>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "start",
          height: "100%",
        }}
      >
        <List>
          {navItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => navigate(item.path)}
                sx={{
                  gap: 1,
                  px: 2,
                  "&.Mui-selected": {
                    backgroundColor: theme.palette.action.selected,
                  },
                  "&:hover": {
                    backgroundColor: theme.palette.action.hover,
                  },
                }}
              >
                <ListItemIcon sx={{ color: theme.palette.text.primary, minWidth: 30 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar;