// DataTable.tsx
import React, { useState, useMemo } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  IconButton,
  useTheme,
  TextField,
  TablePagination,
  InputAdornment,
} from "@mui/material";
import AddCircleOutlineRoundedIcon from "@mui/icons-material/AddCircleOutlineRounded";
import SearchIcon from "@mui/icons-material/Search";
import DownloadIcon from "@mui/icons-material/Download";

export type ColumnDef<T> = {
  label: string;
  accessor?: keyof T;
  render?: (row: T) => React.ReactNode;
};

interface DataTableProps<T extends { id: string | number }> {
  title: string;
  columns: ColumnDef<T>[];
  data: T[];
  onAddClick?: () => void;
  onExportClick?: () => void;
}

function DataTable<T extends { id: string | number }>({
  title,
  columns,
  data,
  onAddClick,
  onExportClick,
}: DataTableProps<T>) {
  const theme = useTheme();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const filteredData = useMemo(() => {
    if (!search.trim()) return data;
    return data.filter((row) =>
      Object.values(row).some((value) =>
        String(value).toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [data, search]);

  const paginatedData = useMemo(() => {
    const start = page * rowsPerPage;
    return filteredData.slice(start, start + rowsPerPage);
  }, [filteredData, page, rowsPerPage]);

  return (
    <TableContainer
      component={Paper}
      sx={{
        mt: 4,
        borderRadius: 2,
        boxShadow: 3,
        backgroundColor: "#fff",
      }}
    >
      <Box
        px={2}
        py={2}
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderBottom: `1px solid ${theme.palette.divider}`,
          flexWrap: "wrap",
          gap: 2,
        }}
      >
        <Box>
          <Typography variant="h6" sx={{ color: "#000", fontWeight: 'bold' }}>{title}</Typography>
          <Typography
            variant="caption"
            sx={{ fontStyle: "italic", color: theme.palette.text.secondary }}
          >
            List of all records with actions and filters
          </Typography>
        </Box>

        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        <TextField
            size="small"
            placeholder="Search..."
            variant="outlined"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ color: "#000" }} />
                </InputAdornment>
              ),
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                color: "#000",
                '& fieldset': {
                  borderColor: '#ccc',
                },
                '&:hover fieldset': {
                  borderColor: '#000',
                },
                '&.Mui-focused fieldset': {
                  borderColor: theme => theme.palette.primary.main,
                },
              },
              input: { color: "#000" },
            }}
          />
          {onExportClick && (
            <IconButton onClick={onExportClick} color="primary">
              <DownloadIcon />
            </IconButton>
          )}
          {onAddClick && (
            <IconButton onClick={onAddClick} color="primary">
              <AddCircleOutlineRoundedIcon />
            </IconButton>
          )}
        </Box>
      </Box>

      <Table>
        <TableHead>
          <TableRow>
            {columns.map((col, index) => (
              <TableCell
                key={index}
                sx={{
                  fontWeight: 700,
                  color: "#000",
                  textTransform: "uppercase",
                  fontSize: "0.85rem",
                  backgroundColor: "transparent",
                }}
              >
                {col.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {paginatedData.map((row, rowIndex) => (
            <TableRow
              key={row.id}
              hover
              sx={{
                backgroundColor: rowIndex % 2 === 0 ? "#fafafa" : "#fff",
                transition: "background-color 0.2s ease",
                "&:hover": {
                  backgroundColor: theme.palette.action.hover,
                },
              }}
            >
              {columns.map((col, index) => (
                <TableCell key={index} sx={{ color: "#000", fontSize: "0.95rem" }}>
                  {col.render ? col.render(row) : String(row[col.accessor!] ?? "-")}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <TablePagination
        component="div"
        count={filteredData.length}
        page={page}
        onPageChange={(_, newPage) => setPage(newPage)}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={(e) => {
          setRowsPerPage(parseInt(e.target.value, 10));
          setPage(0);
        }}
        rowsPerPageOptions={[5, 10, 25]}
        sx={{
          color: "#000",
          '.MuiSvgIcon-root': {
            color: "#000",
          },
        }}
      />
    </TableContainer>
  );
}

export default DataTable;
