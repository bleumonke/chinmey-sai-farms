import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  IconButton,
  Skeleton,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import * as XLSX from 'xlsx';

import DataTable, { ColumnDef } from '../../components/DataTable';
import RecordFormDialog from '../../components/RecordFormDialog';
import ConfirmDialog from '../../components/ConfirmDialog';
import Notification from '../../components/Notification';

import {
  getLayouts,
  createLayout,
  updateLayout,
  deleteLayout,
} from '../../api';

interface Layout {
  id: string;
  name?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  area_in_acres?: number;
  center_lat?: number;
  center_lng?: number;
  center_coordinates?: { lat: number; long: number };
  perimeter_coordinates?: { [key: string]: { lat: number; lng: number } };
}

const LayoutsTable: React.FC = () => {
  const [layouts, setLayouts] = useState<Layout[]>([]);
  const [loading, setLoading] = useState(true);
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [selectedLayout, setSelectedLayout] = useState<Layout | null>(null);
  const [formData, setFormData] = useState<any>({});
  const [perimeterCoords, setPerimeterCoords] = useState<{
    [key: string]: { lat: number; lng: number };
  }>({});
  const [notification, setNotification] = useState<{
    message: string;
    severity: 'success' | 'error';
  } | null>(null);

  const fetchLayouts = async () => {
    setLoading(true);
    try {
      const res = await getLayouts();
      setLayouts(res.data);
    } catch {
      showNotification('Failed to fetch layouts', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLayouts();
  }, []);

  const handleOpenForm = (layout?: Layout) => {
    setEditMode(!!layout);
    setSelectedLayout(layout || null);
    setFormData({
      name: layout?.name || '',
      address: layout?.address || '',
      city: layout?.city || '',
      state: layout?.state || '',
      zip_code: layout?.zip_code || '',
      country: layout?.country || '',
      area_in_acres: layout?.area_in_acres?.toString() || '',
      center_lat: layout?.center_coordinates?.lat?.toString() || '',
      center_lng: layout?.center_coordinates?.long?.toString() || '',
    });
    setPerimeterCoords(layout?.perimeter_coordinates || {});
    setFormDialogOpen(true);
  };

  const handleFormChange = (name: string, value: string) => {
    setFormData((prev: any) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async () => {
    try {
      const payload = {
        ...formData,
        area_in_acres: parseFloat(formData.area_in_acres),
        center_coordinates: {
          lat: parseFloat(formData.center_lat),
          long: parseFloat(formData.center_lng),
        },
        perimeter_coordinates: perimeterCoords,
      };

      if (editMode && selectedLayout) {
        await updateLayout(selectedLayout.id, payload);
        showNotification('Layout updated', 'success');
      } else {
        await createLayout(payload);
        showNotification('Layout created', 'success');
      }

      setFormDialogOpen(false);
      fetchLayouts();
    } catch {
      showNotification('Invalid coordinates or failed operation', 'error');
    }
  };

  const handleConfirmDelete = (layout: Layout) => {
    setSelectedLayout(layout);
    setConfirmDialogOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedLayout) return;
    try {
      await deleteLayout(selectedLayout.id);
      showNotification('Layout deleted', 'success');
      setConfirmDialogOpen(false);
      fetchLayouts();
    } catch {
      showNotification('Delete failed', 'error');
    }
  };

  const handleAddPerimeter = () => {
    const key = `point_${Object.keys(perimeterCoords).length + 1}`;
    setPerimeterCoords({ ...perimeterCoords, [key]: { lat: 0, lng: 0 } });
  };

  const updatePerimeterValue = (
    key: string,
    field: 'lat' | 'lng',
    value: number
  ) => {
    setPerimeterCoords({
      ...perimeterCoords,
      [key]: {
        ...perimeterCoords[key],
        [field]: value,
      },
    });
  };

  const showNotification = (
    message: string,
    severity: 'success' | 'error'
  ) => {
    setNotification({ message, severity });
  };

  const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(
      layouts.map(({ id, perimeter_coordinates, center_coordinates, ...rest }) => rest)
    );
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Layouts');
    XLSX.writeFile(workbook, 'layouts.xlsx');
  };

  const columns: ColumnDef<Layout>[] = [
    { label: 'Name', accessor: 'name' },
    {
      label: 'Address',
      render: (row) =>
        [row.address, row.city, row.state, row.zip_code, row.country]
          .filter(Boolean)
          .join(', '),
    },
    { label: 'Area (Acres)', accessor: 'area_in_acres' },
    {
      label: '',
      render: (row) => (
        <>
          <IconButton
            onClick={() => handleOpenForm(row)}
            color="primary"
          >
            <EditIcon />
          </IconButton>
          <IconButton
            color="error"
            onClick={() => handleConfirmDelete(row)}
          >
            <DeleteIcon />
          </IconButton>
        </>
      ),
    },
  ];

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" fontWeight={600} mb={2}>
        Layouts
      </Typography>

      {loading ? (
        <Box>
          {[1, 2, 3].map((n) => (
            <Skeleton
              key={n}
              variant="rectangular"
              height={80}
              sx={{ my: 1, borderRadius: 2 }}
            />
          ))}
        </Box>
      ) : (
        <DataTable
          title="Layouts"
          columns={columns}
          data={layouts}
          onAddClick={() => handleOpenForm()}
          onExportClick={exportToExcel} // ✅ download icon support
        />
      )}

      <RecordFormDialog
        open={formDialogOpen}
        title={editMode ? 'Edit Layout' : 'Add New Layout'}
        formData={formData}
        fields={[
          { name: 'name', label: 'Name' },
          { name: 'address', label: 'Address' },
          { name: 'city', label: 'City' },
          { name: 'state', label: 'State' },
          { name: 'zip_code', label: 'Zip Code' },
          { name: 'country', label: 'Country' },
          { name: 'area_in_acres', label: 'Area (in acres)' },
          { name: 'center_lat', label: 'Center Latitude' },
          { name: 'center_lng', label: 'Center Longitude' },
        ]}
        extraContent={
          <>
            <Button onClick={handleAddPerimeter}>Add Perimeter Point</Button>
            {Object.entries(perimeterCoords).map(([key, coord]) => (
              <Stack direction="row" spacing={2} key={key} mt={2}>
                <TextField
                  label={`Lat (${key})`}
                  type="number"
                  value={coord.lat}
                  onChange={(e) =>
                    updatePerimeterValue(key, 'lat', parseFloat(e.target.value))
                  }
                />
                <TextField
                  label={`Lng (${key})`}
                  type="number"
                  value={coord.lng}
                  onChange={(e) =>
                    updatePerimeterValue(key, 'lng', parseFloat(e.target.value))
                  }
                />
              </Stack>
            ))}
          </>
        }
        onClose={() => setFormDialogOpen(false)}
        onChange={handleFormChange}
        onSubmit={handleFormSubmit}
        submitLabel={editMode ? 'Update' : 'Create'}
      />

      <ConfirmDialog
        open={confirmDialogOpen}
        message={`Are you sure you want to delete ${selectedLayout?.name}?`}
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

export default LayoutsTable;
