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
  getPaymentModes,
  createPaymentMode,
  updatePaymentMode,
  deletePaymentMode,
} from '../../api';

interface PaymentMode {
  id: string;
  name?: string;
}

const PaymentModesTable: React.FC = () => {
  const [modes, setModes] = useState<PaymentMode[]>([]);
  const [loading, setLoading] = useState(true);
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [selectedMode, setSelectedMode] = useState<PaymentMode | null>(null);
  const [formData, setFormData] = useState({ name: '' });
  const [notification, setNotification] = useState<{ message: string; severity: 'success' | 'error' } | null>(null);

  const fetchModes = async () => {
    setLoading(true);
    try {
      const res = await getPaymentModes();
      setModes(res.data);
    } catch {
      showNotification('Failed to fetch payment modes', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModes();
  }, []);

  const handleOpenForm = (mode?: PaymentMode) => {
    setEditMode(!!mode);
    setSelectedMode(mode || null);
    setFormData({ name: mode?.name || '' });
    setFormDialogOpen(true);
  };

  const handleFormChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async () => {
    try {
      if (editMode && selectedMode) {
        await updatePaymentMode(selectedMode.id, formData);
        showNotification('Payment mode updated', 'success');
      } else {
        await createPaymentMode(formData);
        showNotification('Payment mode created', 'success');
      }
      setFormDialogOpen(false);
      fetchModes();
    } catch {
      showNotification('Operation failed', 'error');
    }
  };

  const handleConfirmDelete = (mode: PaymentMode) => {
    setSelectedMode(mode);
    setConfirmDialogOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedMode) return;
    try {
      await deletePaymentMode(selectedMode.id);
      showNotification('Payment mode deleted', 'success');
      setConfirmDialogOpen(false);
      fetchModes();
    } catch {
      showNotification('Failed to delete payment mode', 'error');
    }
  };

  const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(modes.map(({ id, ...rest }) => rest));
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Payment Modes');
    XLSX.writeFile(workbook, 'payment_modes.xlsx');
  };

  const showNotification = (message: string, severity: 'success' | 'error') => {
    setNotification({ message, severity });
  };

  const columns: ColumnDef<PaymentMode>[] = [
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
      <Typography variant="h5" fontWeight={600} mb={2}>Payment Modes</Typography>

      {loading ? (
        <Box>
          {[1, 2, 3].map((n) => (
            <Skeleton key={n} variant="rectangular" height={80} sx={{ my: 1, borderRadius: 2 }} />
          ))}
        </Box>
      ) : (
        <DataTable
          title="Payment Modes"
          columns={columns}
          data={modes}
          onAddClick={() => handleOpenForm()}
          onExportClick={exportToExcel}
        />
      )}

      <RecordFormDialog
        open={formDialogOpen}
        title={editMode ? 'Edit Payment Mode' : 'Add New Payment Mode'}
        formData={formData}
        fields={[
          { name: 'name', label: 'Name' },
        ]}
        onClose={() => setFormDialogOpen(false)}
        onChange={handleFormChange}
        onSubmit={handleFormSubmit}
        submitLabel={editMode ? 'Update' : 'Create'}
      />

      <ConfirmDialog
        open={confirmDialogOpen}
        message={`Are you sure you want to delete ${selectedMode?.name}?`}
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

export default PaymentModesTable;
