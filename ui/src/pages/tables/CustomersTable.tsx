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
  getCustomers,
  createCustomer,
  updateCustomer,
  deleteCustomer,
} from '../../api';

interface Customer {
  id: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
}

const CustomersTable: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
  });
  const [notification, setNotification] = useState<{ message: string; severity: 'success' | 'error' } | null>(null);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const res = await getCustomers();
      setCustomers(res.data);
    } catch {
      showNotification('Failed to fetch customers', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleOpenForm = (customer?: Customer) => {
    setEditMode(!!customer);
    setSelectedCustomer(customer || null);
    setFormData({
      first_name: customer?.first_name || '',
      last_name: customer?.last_name || '',
      email: customer?.email || '',
      phone: customer?.phone || '',
    });
    setFormDialogOpen(true);
  };

  const handleFormChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async () => {
    try {
      if (editMode && selectedCustomer) {
        await updateCustomer(selectedCustomer.id, formData);
        showNotification('Customer updated', 'success');
      } else {
        await createCustomer(formData);
        showNotification('Customer created', 'success');
      }
      setFormDialogOpen(false);
      fetchCustomers();
    } catch {
      showNotification('Operation failed', 'error');
    }
  };

  const handleConfirmDelete = (customer: Customer) => {
    setSelectedCustomer(customer);
    setConfirmDialogOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedCustomer) return;
    try {
      await deleteCustomer(selectedCustomer.id);
      showNotification('Customer deleted', 'success');
      setConfirmDialogOpen(false);
      fetchCustomers();
    } catch {
      showNotification('Failed to delete customer', 'error');
    }
  };

  const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(customers.map(({ id, ...rest }) => rest));
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Customers');
    XLSX.writeFile(workbook, 'customers.xlsx');
  };

  const showNotification = (message: string, severity: 'success' | 'error') => {
    setNotification({ message, severity });
  };

  const columns: ColumnDef<Customer>[] = [
    { label: 'First Name', accessor: 'first_name' },
    { label: 'Last Name', accessor: 'last_name' },
    { label: 'Email', accessor: 'email' },
    { label: 'Phone', accessor: 'phone' },
    {
      label: '',
      render: (row) => (
        <>
          <IconButton onClick={() => handleOpenForm(row)} color="primary">
            <EditIcon />
          </IconButton>
          <IconButton color="error" onClick={() => handleConfirmDelete(row)}>
            <DeleteIcon />
          </IconButton>
        </>
      ),
    },
  ];

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" fontWeight={600} mb={2}>Customers</Typography>

      {loading ? (
        <Box>
          {[1, 2, 3].map((n) => (
            <Skeleton key={n} variant="rectangular" height={80} sx={{ my: 1, borderRadius: 2 }} />
          ))}
        </Box>
      ) : (
        <DataTable
          title="Customers"
          columns={columns}
          data={customers}
          onAddClick={() => handleOpenForm()}
          onExportClick={exportToExcel}
        />
      )}

      <RecordFormDialog
        open={formDialogOpen}
        title={editMode ? 'Edit Customer' : 'Add New Customer'}
        formData={formData}
        fields={[
          { name: 'first_name', label: 'First Name' },
          { name: 'last_name', label: 'Last Name' },
          { name: 'email', label: 'Email' },
          { name: 'phone', label: 'Phone' },
        ]}
        onClose={() => setFormDialogOpen(false)}
        onChange={handleFormChange}
        onSubmit={handleFormSubmit}
        submitLabel={editMode ? 'Update' : 'Create'}
      />

      <ConfirmDialog
        open={confirmDialogOpen}
        message={`Are you sure you want to delete ${selectedCustomer?.first_name} ${selectedCustomer?.last_name}?`}
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

export default CustomersTable;
