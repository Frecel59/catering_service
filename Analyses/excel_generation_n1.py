# Importation des bibliothèques nécessaires
import io
import pandas as pd

def generate_excel_report_n1(result_df_n1, start_date_a, end_date_a, start_date_a2, end_date_a2, jours_moments_selectionnes_a):
    # Créer un objet BytesIO pour stocker les données Excel
    output = io.BytesIO()



    # Utiliser Pandas pour sauvegarder le DataFrame au format Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df_n1.to_excel(writer, sheet_name='Analyse N vs N-1', startrow=2, index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Analyse N vs N-1']

        # Accédez à la feuille Excel générée pour formater les colonnes
        worksheet = writer.sheets['Analyse N vs N-1']

        # Supprimer l'affichage du quadrillage
        worksheet.hide_gridlines(2)

        # Définit le zoom à 130%
        worksheet.set_zoom(130)

        # Titre
        title_text = f"N : du {start_date_a} au {end_date_a} - N-1 : du {start_date_a2} au {end_date_a2}"
        worksheet.merge_range('A1:F1', title_text, workbook.add_format({
            'bold': True,
            'font_size': 15,
            'fg_color': 'red',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        }))

        # Créer un format personnalisé pour les en-têtes de colonnes
        header_format = writer.book.add_format({
            'bold': True,
            'text_wrap': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'red',
            'font_color': 'white',
            'border': 1,
            'font_size': 12
        })

        # Appliquer le format aux en-têtes de colonnes
        for col_num, value in enumerate(result_df_n1.columns.values):
            worksheet.write(2, col_num, value, header_format)

        # Formatage des cellules pour les 5 premières lignes de chaque colonne
        custom_format = writer.book.add_format({
            'font_size': 11,
            'bold': True,
            'border': 1,
            'fg_color': '#E2E2E2'
        })

        formats = {
            'A': custom_format,
            'B4': writer.book.add_format({'num_format': '#,##0', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'}),
            'D4': writer.book.add_format({'num_format': '0.00%', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'}),
            'B5': writer.book.add_format({'num_format': '#,##0.00 €', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'}),
            'B6': writer.book.add_format({'num_format': '#,##0.00 €', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'})
        }

        for row in range(3, len(result_df_n1) + 3):
            for col, col_format in formats.items():
                worksheet.write(row, ord(col) - 65, result_df_n1.iat[row-3, ord(col) - 65], col_format)

        # Définition de la largeur pour chaque colonne
        worksheet.set_column('A:A', len('Indicateur') + 8)
        worksheet.set_column('B:B', len('N') + 10)
        worksheet.set_column('C:C', len('N-1') + 10)
        worksheet.set_column('D:D', len('Variation') + 10)
        worksheet.set_column('E:E', len('Moyenne N') + 10)
        worksheet.set_column('F:F', len('Moyenne N-1') + 10)

        def dict_to_string_format(jours_moments_dict):
            text_list = [f"{jour.upper()} : {', '.join(moments)}" for jour, moments in jours_moments_dict.items() if moments]

            # Divisez la liste en deux si elle est assez longue
            mid_idx = len(text_list) // 2
            first_half = ' - '.join(text_list[:mid_idx])
            second_half = ' - '.join(text_list[mid_idx:])

            return f"{first_half}\n{second_half}"



        jours_moments_selectionnes_text = dict_to_string_format(jours_moments_selectionnes_a)
        worksheet.merge_range('A10:F11', jours_moments_selectionnes_text, workbook.add_format({
            'text_wrap': True,
            'font_size': 8,
            'fg_color': 'E2E2E2',
            'font_color': 'black',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        }))

    # Définir le point de départ pour la lecture
    output.seek(0)

    return output
