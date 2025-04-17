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
  getExtentRanges,
  createExtentRange,
  updateExtentRange,
  deleteExtentRange,
} from '../../api';

interface ExtentRange {
  id: string;
  label?: string;
  unit?: string;
  min_value?: number;
  max_value?: number;
}

const ExtentRangesTable: React.FC = () => {
  const [ranges, setRanges] = useState<ExtentRange[]>([]);
  const [loading, setLoading] = useState(true);
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [selectedRange, setSelectedRange] = useState<ExtentRange | null>(null);
  const [formData, setFormData] = useState({
    label: '',
    unit: '',
    min_value: '',
    max_value: '',
  });
  const [notification, setNotification] = useState<{ message: string; severity: 'success' | 'error' } | null>(null);

  const fetchRanges = async () => {
    setLoading(true);
    try {
      const res = await getExtentRanges();
      setRanges(res.data);
    } catch {
      showNotification('Failed to fetch extent ranges', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRanges();
  }, []);

  const handleOpenForm = (range?: ExtentRange) => {
    setEditMode(!!range);
    setSelectedRange(range || null);
    setFormData({
      label: range?.label || '',
      unit: range?.unit || '',
      min_value: range?.min_value?.toString() || '',
      max_value: range?.max_value?.toString() || '',
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
        min_value: parseFloat(formData.min_value),
        max_value: parseFloat(formData.max_value),
      };

      if (editMode && selectedRange) {
        await updateExtentRange(selectedRange.id, payload);
        showNotification('Extent range updated', 'success');
      } else {
        await createExtentRange(payload);
        showNotification('Extent range created', 'success');
      }

      setFormDialogOpen(false);
      fetchRanges();
    } catch {
      showNotification('Operation failed', 'error');
    }
  };

  const handleConfirmDelete = (range: ExtentRange) => {
    setSelectedRange(range);
    setConfirmDialogOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedRange) return;
    try {
      await deleteExtentRange(selectedRange.id);
      showNotification('Extent range deleted', 'success');
      setConfirmDialogOpen(false);
      fetchRanges();
    } catch {
      showNotification('Failed to delete extent range', 'error');
    }
  };

  const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(ranges.map(({ id, ...rest }) => rest));
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Extent Ranges');
    XLSX.writeFile(workbook, 'extent_ranges.xlsx');
  };

  const showNotification = (message: string, severity: 'success' | 'error') => {
    setNotification({ message, severity });
  };

  const columns: ColumnDef<ExtentRange>[] = [
    { label: 'Label', accessor: 'label' },
    { label: 'Unit', accessor: 'unit' },
    { label: 'Min Value', accessor: 'min_value' },
    { label: 'Max Value', accessor: 'max_value' },
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
      <Typography variant="h5" fontWeight={600} mb={2}>Extent Ranges</Typography>

      {loading ? (
        <Box>
          {[1, 2, 3].map((n) => (
            <Skeleton key={n} variant="rectangular" height={80} sx={{ my: 1, borderRadius: 2 }} />
          ))}
        </Box>
      ) : (
        <DataTable
          title="Extent Ranges"
          columns={columns}
          data={ranges}
          onAddClick={() => handleOpenForm()}
          onExportClick={exportToExcel}
        />
      )}

      <RecordFormDialog
        open={formDialogOpen}
        title={editMode ? 'Edit Range' : 'Add New Range'}
        formData={formData}
        fields={[
          { name: 'label', label: 'Label' },
          { name: 'unit', label: 'Unit' },
          { name: 'min_value', label: 'Min Value' },
          { name: 'max_value', label: 'Max Value' },
        ]}
        onClose={() => setFormDialogOpen(false)}
        onChange={handleFormChange}
        onSubmit={handleFormSubmit}
        submitLabel={editMode ? 'Update' : 'Create'}
      />

      <ConfirmDialog
        open={confirmDialogOpen}
        message={`Are you sure you want to delete ${selectedRange?.label}?`}
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

export default ExtentRangesTable;
