import React from "react";
import LayoutsTable from "./tables/LayoutsTable";
import PlotsTable from "./tables/PlotsTable";

const Layouts: React.FC = () => {
  return (
    <div>
      <h1>Layouts</h1>
      <LayoutsTable />
      <h2>Plots</h2>
      <PlotsTable />
    </div>
  );
};

export default Layouts;