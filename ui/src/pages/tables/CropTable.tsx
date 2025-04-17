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
  getCrops,
  createCrop,
  updateCrop,
  deleteCrop,
} from '../../api';

interface Crop {
  id: string;
  name?: string;
}

const CropsTable: React.FC = () => {
  const [crops, setCrops] = useState<Crop[]>([]);
  const [loading, setLoading] = useState(true);
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [selectedCrop, setSelectedCrop] = useState<Crop | null>(null);
  const [formData, setFormData] = useState({ name: '' });
  const [notification, setNotification] = useState<{ message: string; severity: 'success' | 'error' } | null>(null);

  const fetchCrops = async () => {
    setLoading(true);
    try {
      const res = await getCrops();
      setCrops(res.data);
    } catch {
      showNotification('Failed to fetch crops', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCrops();
  }, []);

  const handleOpenForm = (crop?: Crop) => {
    setEditMode(!!crop);
    setSelectedCrop(crop || null);
    setFormData({ name: crop?.name || '' });
    setFormDialogOpen(true);
  };

  const handleFormChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async () => {
    try {
      if (editMode && selectedCrop) {
        await updateCrop(selectedCrop.id, formData);
        showNotification('Crop updated', 'success');
      } else {
        await createCrop(formData);
        showNotification('Crop created', 'success');
      }
      setFormDialogOpen(false);
      fetchCrops();
    } catch {
      showNotification('Operation failed', 'error');
    }
  };

  const handleConfirmDelete = (crop: Crop) => {
    setSelectedCrop(crop);
    setConfirmDialogOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedCrop) return;
    try {
      await deleteCrop(selectedCrop.id);
      showNotification('Crop deleted', 'success');
      setConfirmDialogOpen(false);
      fetchCrops();
    } catch {
      showNotification('Failed to delete crop', 'error');
    }
  };

  const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(crops.map(({ id, ...rest }) => rest));
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Crops');
    XLSX.writeFile(workbook, 'crops.xlsx');
  };

  const showNotification = (message: string, severity: 'success' | 'error') => {
    setNotification({ message, severity });
  };

  const columns: ColumnDef<Crop>[] = [
    { label: 'Name', accessor: 'name' },
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
      <Typography variant="h5" fontWeight={600} mb={2}>Crops</Typography>

      {loading ? (
        <Box>
          {[1, 2, 3].map((n) => (
            <Skeleton key={n} variant="rectangular" height={80} sx={{ my: 1, borderRadius: 2 }} />
          ))}
        </Box>
      ) : (
        <DataTable
          title="Crops"
          columns={columns}
          data={crops}
          onAddClick={() => handleOpenForm()}
          onExportClick={exportToExcel}
        />
      )}

      <RecordFormDialog
        open={formDialogOpen}
        title={editMode ? 'Edit Crop' : 'Add New Crop'}
        formData={formData}
        fields={[{ name: 'name', label: 'Name' }]}
        onClose={() => setFormDialogOpen(false)}
        onChange={handleFormChange}
        onSubmit={handleFormSubmit}
        submitLabel={editMode ? 'Update' : 'Create'}
      />

      <ConfirmDialog
        open={confirmDialogOpen}
        message={`Are you sure you want to delete ${selectedCrop?.name}?`}
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

export default CropsTable;
