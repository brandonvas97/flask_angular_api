import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { map } from 'rxjs/operators';
import { catchError } from 'rxjs/internal/operators/catchError';
import { HttpHeaders, HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BookServiceService {
  //private BASE_URL = 'http://backend:5000/'
  private BASE_URL = `http://${window.location.hostname}:5000/`
  
  constructor( private httpClient: HttpClient) { }

  private ReturnResponseData(response: any) {
    return response;
  }
  
  private handleError(error: any) {
    return throwError(error);
  }

  listBooks():Observable<any>{
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      }),
      observe: "response" as 'body'};
    return this.httpClient.get(`${this.BASE_URL}all`, httpOptions).pipe(map((response: any) => this.ReturnResponseData(response)),catchError(this.handleError));
  }

  listBookById(id:any):Observable<any>{
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      }),
      observe: "response" as 'body'};
    return this.httpClient.get(`${this.BASE_URL}list/${id}`, httpOptions).pipe(map((response: any) => this.ReturnResponseData(response)),catchError(this.handleError));
  }

  addBook(title:any, author:any, read:any):Observable<any>{
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }), 
      observe: "response" as 'body'
    };
    //console.log("body: ", {"title": title, "author": author, "read":read})
    return this.httpClient.post(`${this.BASE_URL}add`, {"title": title, "author": author, "read":read}, httpOptions).pipe(
      map((response: any) => this.ReturnResponseData(response)),
      catchError(this.handleError));
  }

  editBook(id:any, title:any, author:any, read:any):Observable<any>{
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }), 
      observe: "response" as 'body'
    };
    //console.log("body: ", {"title": title, "author": author, "read":read})
    return this.httpClient.put(`${this.BASE_URL}edit/${id}`, {"title": title, "author": author, "read":read}, httpOptions).pipe(
      map((response: any) => this.ReturnResponseData(response)),
      catchError(this.handleError));
  }

  deleteBook(id:any):Observable<any>{
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }), 
      observe: "response" as 'body'
    };
    return this.httpClient.delete(`${this.BASE_URL}delete/${id}`, httpOptions).pipe(
      map((response: any) => this.ReturnResponseData(response)),
      catchError(this.handleError));
  }
}
