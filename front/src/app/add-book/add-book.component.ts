import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { BookServiceService } from '../book-service.service';

@Component({
  selector: 'app-add-book',
  templateUrl: './add-book.component.html',
  styleUrls: ['./add-book.component.scss']
})
export class AddBookComponent implements OnInit {

  addBookForm: bookForm = new bookForm();
  

  @ViewChild("bookForm")
  bookForm!: NgForm;
  isSubmitted: boolean = false;
  constructor(private router: Router, private bookService: BookServiceService, private toastr: ToastrService) { }

  ngOnInit(): void {  }

  AddBook(isValid: any) {
    this.isSubmitted = true;
    if (isValid) {
      this.bookService.addBook(this.addBookForm.title, this.addBookForm.author, this.addBookForm.read).subscribe(async data => {
        if (data != null && data.body != null) {
          if (data != null && data.body != null) {
            var resultData = data.body;
            if (resultData != null) {
              this.toastr.success("Book registered successfully");
              setTimeout(() => {
                this.router.navigate(['/']);
              }, 500);
            }
          }
        }
      },
        async error => {
          this.toastr.error("Error when trying to register the book");
          setTimeout(() => {
            this.router.navigate(['/']);
          }, 500);
        });
    }
  }

}

export class bookForm {
  title:any;
  author:any;
  read:boolean;

  constructor(data?: Partial<bookForm>) {
    this.title = data?.title || '';
    this.author = data?.author || '';
    this.read = data?.read === true; // Ensure read is always a boolean
  }
}