import React from "react";
import { Box, Grid } from "@mui/material";
import CropTable from "./tables/CropTable";
import ExtentRangesTable from "./tables/ExtentRangeTable";
import PaymentModesTable from "./tables/PaymentsModeTable";

const Settings: React.FC = () => {
  return (
    <Grid container spacing={2}>
      <Grid size={8}>
        <CropTable />
      </Grid>
      <Grid size={8}>
        <ExtentRangesTable />
      </Grid>
      <Grid size={8}>
        <PaymentModesTable />
      </Grid>
    </Grid>
  );
};

export default Settings;
