// Plots.tsx
import React, { useEffect, useState } from 'react';
import { Box, IconButton, Skeleton, Typography } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import * as XLSX from 'xlsx';

import DataTable, { ColumnDef } from '../../components/DataTable';
import RecordFormDialog from '../../components/RecordFormDialog';
import ConfirmDialog from '../../components/ConfirmDialog';
import Notification from '../../components/Notification';

import {
  getPlots,
  createPlot,
  updatePlot,
  deletePlot,
} from '../../api';

interface Plot {
  id: string;
  name?: string;
  number?: string;
  layout_id?: string;
  area_in_acres?: number;
  is_active?: boolean;
  is_sold?: boolean;
}

const PlotsTable: React.FC = () => {
  const [plots, setPlots] = useState<Plot[]>([]);
  const [loading, setLoading] = useState(true);
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [selectedPlot, setSelectedPlot] = useState<Plot | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    number: '',
    area_in_acres: '',
  });
  const [notification, setNotification] = useState<{ message: string; severity: 'success' | 'error' } | null>(null);

  const fetchPlots = async () => {
    setLoading(true);
    try {
      const res = await getPlots();
      setPlots(res.data);
    } catch {
      showNotification('Failed to fetch plots', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlots();
  }, []);

  const handleOpenForm = (plot?: Plot) => {
    setEditMode(!!plot);
    setSelectedPlot(plot || null);
    setFormData({
      name: plot?.name || '',
      number: plot?.number || '',
      area_in_acres: plot?.area_in_acres?.toString() || '',
    });
    setFormDialogOpen(true);
  };

  const handleFormChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async () => {
    try {
      const payload = {
        ...formData,
        area_in_acres: parseFloat(formData.area_in_acres),
      };

      if (editMode && selectedPlot) {
        await updatePlot(selectedPlot.id, payload);
        showNotification('Plot updated', 'success');
      } else {
        await createPlot(payload);
        showNotification('Plot created', 'success');
      }
      setFormDialogOpen(false);
      fetchPlots();
    } catch {
      showNotification('Operation failed', 'error');
    }
  };

  const handleConfirmDelete = (plot: Plot) => {
    setSelectedPlot(plot);
    setConfirmDialogOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedPlot) return;
    try {
      await deletePlot(selectedPlot.id);
      showNotification('Plot deleted', 'success');
      setConfirmDialogOpen(false);
      fetchPlots();
    } catch {
      showNotification('Failed to delete plot', 'error');
    }
  };

  const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(plots.map(({ id, ...rest }) => rest));
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Plots');
    XLSX.writeFile(workbook, 'plots.xlsx');
  };

  const showNotification = (message: string, severity: 'success' | 'error') => {
    setNotification({ message, severity });
  };

  const columns: ColumnDef<Plot>[] = [
    { label: 'Name', accessor: 'name' },
    { label: 'Number', accessor: 'number' },
    { label: 'Area (acres)', accessor: 'area_in_acres' },
    {
      label: '',
      render: (row) => (
        <>
          <IconButton onClick={() => handleOpenForm(row)} color="primary"><EditIcon /></IconButton>
          <IconButton color="error" onClick={() => handleConfirmDelete(row)}><DeleteIcon /></IconButton>
        </>
      ),
    },
  ];

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" fontWeight={600} mb={2}>Plots</Typography>

      {loading ? (
        <Box>
          {[1, 2, 3].map((n) => (
            <Skeleton key={n} variant="rectangular" height={80} sx={{ my: 1, borderRadius: 2 }} />
          ))}
        </Box>
      ) : (
        <DataTable
          title="Plots"
          columns={columns}
          data={plots}
          onAddClick={() => handleOpenForm()}
          onExportClick={exportToExcel}
        />
      )}

      <RecordFormDialog
        open={formDialogOpen}
        title={editMode ? 'Edit Plot' : 'Add New Plot'}
        formData={formData}
        fields={[
          { name: 'name', label: 'Name' },
          { name: 'number', label: 'Number' },
          { name: 'area_in_acres', label: 'Area (in acres)' },
        ]}
        onClose={() => setFormDialogOpen(false)}
        onChange={handleFormChange}
        onSubmit={handleFormSubmit}
        submitLabel={editMode ? 'Update' : 'Create'}
      />

      <ConfirmDialog
        open={confirmDialogOpen}
        message={`Are you sure you want to delete ${selectedPlot?.name}?`}
        onClose={() => setConfirmDialogOpen(false)}
        onConfirm={handleDelete}
      />

      {notification && (
        <Notification
          open={!!notification}
          message={notification.message}
          severity={notification.severity}
          onClose={() => setNotification(null)}
        />
      )}
    </Box>
  );
};

export default PlotsTable;